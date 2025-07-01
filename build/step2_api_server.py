#!/usr/bin/env python3
"""
Step 2: Workflow API Server (EXE 빌드용)
워크플로우 실행을 관리하는 API 서버

빌드 방법:
pip install pyinstaller flask flask-cors
pyinstaller --onefile --name "Step2_API_Server" --hidden-import=flask --hidden-import=flask_cors step2_api_server.py
"""

import os
import sys
import json
import time
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List
from queue import Queue
from threading import Thread, Lock
import uuid

from flask import Flask, request, jsonify
from flask_cors import CORS

# ==================== 설정 변수 (여기만 수정하세요) ====================

# 서버 설정
SERVER_HOST = '0.0.0.0'  # 모든 IP에서 접속 가능
SERVER_PORT = 5001
SERVER_DEBUG = False  # 프로덕션에서는 False

# 워크플로우 설정
WORKFLOW_BASE_PATH = '../step3_workflows'  # 워크플로우 폴더 경로
DEFAULT_WORKFLOW = 'create_contents'  # 기본 워크플로우
WORKFLOW_TIMEOUT = 300  # 워크플로우 실행 제한 시간 (초)

# 워크플로우 매핑
WORKFLOW_MAPPING = {
    'create_contents_on_user_idea': 'create_contents',
    # 추가 매핑은 여기에
}

# 로그 설정
LOG_DIR = 'logs'  # 로그 디렉토리
LOG_FILE = 'step2_api_server.log'
LOG_LEVEL = logging.INFO
LOG_RETENTION_DAYS = 1  # 로그 보관 일수

# 큐 설정
MAX_QUEUE_SIZE = 100  # 최대 큐 크기
WORKER_THREADS = 2  # 워커 스레드 수

# ========================================================================

# 로그 디렉토리 생성
def create_log_directory():
    """로그 디렉토리 생성"""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

# 오래된 로그 파일 정리
def cleanup_old_logs():
    """오래된 로그 파일 삭제"""
    try:
        log_path = os.path.join(LOG_DIR, LOG_FILE)
        if os.path.exists(log_path):
            # 파일 수정 시간 확인
            file_modified_time = datetime.fromtimestamp(os.path.getmtime(log_path))
            current_time = datetime.now()
            
            # 하루 이상 지난 로그 파일 삭제
            if (current_time - file_modified_time).days >= LOG_RETENTION_DAYS:
                os.remove(log_path)
                print(f"Old log file deleted: {log_path}")
    except Exception as e:
        print(f"Error cleaning up logs: {e}")

# 로깅 설정
def setup_logging():
    """로깅 설정"""
    create_log_directory()
    cleanup_old_logs()
    
    log_path = os.path.join(LOG_DIR, LOG_FILE)
    
    # 로그 포맷터
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 파일 핸들러
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # 로거 설정
    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()

# Flask 앱 생성
app = Flask(__name__)
CORS(app)

# 워크플로우 큐 관리
class WorkflowQueue:
    def __init__(self):
        self.queue = Queue(maxsize=MAX_QUEUE_SIZE)
        self.running_jobs = {}
        self.completed_jobs = {}
        self.lock = Lock()
        self.worker_threads = []
        
    def add_job(self, workflow_id: str, params: dict = None) -> str:
        """워크플로우 작업을 큐에 추가"""
        job_id = str(uuid.uuid4())
        job = {
            'id': job_id,
            'workflow_id': workflow_id,
            'params': params or {},
            'status': 'queued',
            'created_at': datetime.now().isoformat(),
            'started_at': None,
            'completed_at': None,
            'result': None,
            'error': None
        }
        
        with self.lock:
            if self.queue.full():
                raise Exception("Queue is full")
            self.queue.put(job)
            self.completed_jobs[job_id] = job
            
        logger.info(f"Job {job_id} added: {workflow_id}")
        return job_id
    
    def get_job_status(self, job_id: str) -> Optional[dict]:
        """작업 상태 조회"""
        with self.lock:
            return self.completed_jobs.get(job_id)
    
    def get_queue_status(self) -> dict:
        """큐 상태 조회"""
        with self.lock:
            running_count = len([j for j in self.completed_jobs.values() 
                               if j['status'] == 'running'])
            completed_count = len([j for j in self.completed_jobs.values() 
                                 if j['status'] == 'completed'])
            
            return {
                'queue_size': self.queue.qsize(),
                'is_running': running_count > 0,
                'running_count': running_count,
                'total_completed': completed_count,
                'max_queue_size': MAX_QUEUE_SIZE
            }

# 전역 큐 인스턴스
workflow_queue = WorkflowQueue()

def get_workflow_path(workflow_id: str) -> Path:
    """워크플로우 경로 가져오기"""
    # 실행 파일 위치 기준으로 경로 설정
    if getattr(sys, 'frozen', False):
        # PyInstaller로 빌드된 경우
        base_path = Path(sys.executable).parent
    else:
        # 개발 환경
        base_path = Path(__file__).parent
    
    workflow_path = base_path / WORKFLOW_BASE_PATH / workflow_id
    return workflow_path

def execute_workflow(job: dict):
    """워크플로우 실행"""
    try:
        with workflow_queue.lock:
            job['status'] = 'running'
            job['started_at'] = datetime.now().isoformat()
        
        workflow_id = job['workflow_id']
        params = job['params']
        
        logger.info(f"Executing workflow: {workflow_id}")
        
        # 워크플로우 경로 확인
        workflow_path = get_workflow_path(workflow_id)
        
        if not workflow_path.exists():
            raise Exception(f"Workflow not found: {workflow_id}")
        
        # 파라미터 저장
        data_file = workflow_path / "_data.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(params, f, ensure_ascii=False, indent=2)
        
        # main.py 실행
        main_py = workflow_path / "main.py"
        if main_py.exists():
            process = subprocess.run(
                [sys.executable, str(main_py)],
                capture_output=True,
                text=True,
                cwd=str(workflow_path),
                timeout=WORKFLOW_TIMEOUT
            )
            
            if process.returncode == 0:
                try:
                    result = json.loads(process.stdout)
                except:
                    result = {
                        'status': 'completed',
                        'output': process.stdout
                    }
                
                with workflow_queue.lock:
                    job['status'] = 'completed'
                    job['result'] = result
            else:
                raise Exception(f"Workflow failed: {process.stderr}")
        else:
            # 간단한 텍스트 저장 워크플로우 (테스트용)
            output_dir = workflow_path / "output"
            output_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = output_dir / f"result_{timestamp}.txt"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Workflow: {workflow_id}\n")
                f.write(f"Executed at: {datetime.now()}\n")
                f.write(f"Parameters:\n{json.dumps(params, ensure_ascii=False, indent=2)}\n")
            
            with workflow_queue.lock:
                job['status'] = 'completed'
                job['result'] = {
                    'status': 'completed',
                    'output_file': str(output_file)
                }
        
        logger.info(f"Job {job['id']} completed successfully")
        
    except subprocess.TimeoutExpired:
        logger.error(f"Job {job['id']} timeout")
        with workflow_queue.lock:
            job['status'] = 'failed'
            job['error'] = 'Workflow execution timeout'
    except Exception as e:
        logger.error(f"Job {job['id']} failed: {str(e)}")
        with workflow_queue.lock:
            job['status'] = 'failed'
            job['error'] = str(e)
    finally:
        with workflow_queue.lock:
            job['completed_at'] = datetime.now().isoformat()

def worker_thread():
    """워커 스레드 - 큐에서 작업을 가져와 실행"""
    logger.info("Worker thread started")
    
    last_cleanup = datetime.now()
    
    while True:
        try:
            job = workflow_queue.queue.get(timeout=1)
            execute_workflow(job)
            
            # 하루에 한 번 로그 정리
            current_time = datetime.now()
            if (current_time - last_cleanup).days >= 1:
                cleanup_old_logs()
                last_cleanup = current_time
                logger.info("🧹 로그 파일 정리 완료")
        except:
            # 큐가 비어있으면 계속 대기
            time.sleep(0.1)

# API 엔드포인트
@app.route('/')
def index():
    """API 정보"""
    return jsonify({
        'name': 'Workflow Automation API',
        'version': '2.0',
        'status': 'running',
        'endpoints': {
            'GET /status': '시스템 상태',
            'GET /workflows': '워크플로우 목록',
            'POST /workflows/{id}/run': '워크플로우 실행',
            'GET /jobs/{id}': '작업 상태 조회'
        }
    })

@app.route('/status', methods=['GET'])
def get_status():
    """시스템 상태"""
    status = workflow_queue.get_queue_status()
    
    # 최근 작업 10개
    recent_jobs = []
    with workflow_queue.lock:
        sorted_jobs = sorted(
            workflow_queue.completed_jobs.items(),
            key=lambda x: x[1]['created_at'],
            reverse=True
        )[:10]
        
        for job_id, job in sorted_jobs:
            recent_jobs.append({
                'id': job_id,
                'workflow_id': job['workflow_id'],
                'status': job['status'],
                'created_at': job['created_at']
            })
    
    return jsonify({
        'success': True,
        'status': status,
        'recent_jobs': recent_jobs,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/workflows', methods=['GET'])
def list_workflows():
    """워크플로우 목록"""
    try:
        workflows = []
        workflow_base = get_workflow_path('')
        
        if workflow_base.exists():
            for item in workflow_base.iterdir():
                if item.is_dir() and not item.name.startswith('_'):
                    workflows.append({
                        'id': item.name,
                        'name': item.name.replace('_', ' ').title(),
                        'available': True
                    })
        
        return jsonify({
            'success': True,
            'workflows': workflows
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/workflows/<workflow_id>/run', methods=['POST'])
def run_workflow(workflow_id):
    """워크플로우 실행"""
    try:
        params = request.json or {}
        
        # API 타입으로 워크플로우 매핑
        api_type = params.get('api_type')
        if api_type and api_type in WORKFLOW_MAPPING:
            workflow_id = WORKFLOW_MAPPING[api_type]
            logger.info(f"Mapped {api_type} to workflow {workflow_id}")
        
        # 워크플로우 존재 확인
        workflow_path = get_workflow_path(workflow_id)
        if not workflow_path.exists():
            return jsonify({
                'success': False,
                'error': f'Workflow not found: {workflow_id}'
            }), 404
        
        # 큐에 추가
        job_id = workflow_queue.add_job(workflow_id, params)
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'message': 'Workflow queued for execution',
            'status_url': f'/jobs/{job_id}'
        })
        
    except Exception as e:
        logger.error(f"Error running workflow: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """작업 상태 조회"""
    job = workflow_queue.get_job_status(job_id)
    
    if not job:
        return jsonify({
            'success': False,
            'error': 'Job not found'
        }), 404
    
    return jsonify({
        'success': True,
        'job': job
    })

def start_workers():
    """워커 스레드 시작"""
    for i in range(WORKER_THREADS):
        thread = Thread(target=worker_thread, daemon=True)
        thread.start()
        workflow_queue.worker_threads.append(thread)
        logger.info(f"Started worker thread {i+1}")

def main():
    """메인 함수"""
    logger.info("=" * 60)
    logger.info("🚀 Workflow API Server Starting")
    logger.info(f"📡 Server: http://{SERVER_HOST}:{SERVER_PORT}")
    logger.info(f"📂 Workflow Path: {WORKFLOW_BASE_PATH}")
    logger.info(f"👷 Worker Threads: {WORKER_THREADS}")
    logger.info(f"📂 로그 위치: {os.path.join(LOG_DIR, LOG_FILE)}")
    logger.info("=" * 60)
    
    # 워커 스레드 시작
    start_workers()
    
    # Flask 서버 실행
    try:
        app.run(
            host=SERVER_HOST,
            port=SERVER_PORT,
            debug=SERVER_DEBUG,
            use_reloader=False  # PyInstaller와 충돌 방지
        )
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
