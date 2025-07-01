#!/usr/bin/env python3
"""
Step 1: Supabase Polling Service (EXE 빌드용) - 설정 파일 사용 버전
Supabase에서 데이터를 가져와 Step 2 API로 전송하는 폴링 서비스

빌드 방법:
pip install pyinstaller requests
pyinstaller --onefile --name "Step1_Supabase_Polling" step1_polling_service.py
"""

import json
import time
import requests
import logging
import configparser
from datetime import datetime
import sys
import os
from typing import Dict, List, Optional
from pathlib import Path

# 설정 파일 읽기
def load_config():
    """설정 파일 로드"""
    config = configparser.ConfigParser()
    
    # 실행 파일 위치 기준으로 설정 파일 찾기
    if getattr(sys, 'frozen', False):
        # PyInstaller로 빌드된 경우
        config_path = Path(sys.executable).parent / 'config_step1.ini'
    else:
        # 개발 환경
        config_path = Path(__file__).parent / 'config_step1.ini'
    
    if not config_path.exists():
        print(f"ERROR: 설정 파일을 찾을 수 없습니다: {config_path}")
        print("config_step1.ini 파일을 생성해주세요.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    config.read(config_path, encoding='utf-8')
    return config

# 설정 로드
try:
    config = load_config()
    
    # Supabase 설정
    SUPABASE_URL = config.get('supabase', 'url')
    SUPABASE_KEY = config.get('supabase', 'key')
    
    # 테이블 및 컬럼 설정
    TABLE_NAME = config.get('supabase', 'table_name')
    COLUMN_IS_FETCHED = config.get('supabase', 'column_is_fetched')
    COLUMN_IS_AUTO_CREATED = config.get('supabase', 'column_is_auto_created')
    COLUMN_ID = config.get('supabase', 'column_id')
    COLUMN_TITLE_KO = config.get('supabase', 'column_title_ko')
    COLUMN_TITLE_VI = config.get('supabase', 'column_title_vi')
    
    # API 설정
    STEP2_API_URL = config.get('api', 'step2_url')
    API_TYPE = config.get('api', 'api_type')
    
    # 폴링 설정
    POLLING_INTERVAL = config.getint('polling', 'interval_seconds')
    BATCH_SIZE = config.getint('polling', 'batch_size')
    RETRY_DELAY = config.getint('polling', 'retry_delay_seconds')
    
    # 로그 설정
    LOG_LEVEL = getattr(logging, config.get('logging', 'log_level', fallback='INFO'))
    LOG_RETENTION_DAYS = config.getint('logging', 'log_retention_days')
    
except Exception as e:
    print(f"ERROR: 설정 파일 읽기 실패: {e}")
    print("config_step1.ini 파일을 확인해주세요.")
    input("Press Enter to exit...")
    sys.exit(1)

# 로그 설정
LOG_DIR = 'logs'
LOG_FILE = 'step1_polling.log'

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
            file_modified_time = datetime.fromtimestamp(os.path.getmtime(log_path))
            current_time = datetime.now()
            
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
    
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()

class SupabasePoller:
    """Supabase 폴링 서비스"""
    
    def __init__(self):
        self.headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json'
        }
        self.processed_count = 0
        self.error_count = 0
        
    def fetch_unfetched_ideas(self) -> List[Dict]:
        """미처리 데이터 가져오기"""
        try:
            url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}"
            params = {
                f'{COLUMN_IS_AUTO_CREATED}': 'eq.false',
                f'{COLUMN_IS_FETCHED}': 'eq.false',
                'select': '*',
                'order': 'created_at.asc',
                'limit': BATCH_SIZE
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            ideas = response.json()
            if ideas:
                logger.info(f"✅ {len(ideas)}개의 새 데이터 발견")
            return ideas
            
        except Exception as e:
            logger.error(f"❌ 데이터 조회 실패: {str(e)}")
            return []
    
    def update_is_fetched(self, idea_id: int) -> bool:
        """is_fetched 플래그 업데이트"""
        try:
            url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}?{COLUMN_ID}=eq.{idea_id}"
            data = {COLUMN_IS_FETCHED: True}
            
            headers = self.headers.copy()
            headers['Prefer'] = 'return=minimal'
            
            response = requests.patch(url, headers=headers, json=data)
            response.raise_for_status()
            
            logger.info(f"✅ ID {idea_id}의 {COLUMN_IS_FETCHED} 업데이트 완료")
            return True
            
        except Exception as e:
            logger.error(f"❌ ID {idea_id} 업데이트 실패: {str(e)}")
            return False
    
    def send_to_step2(self, idea: Dict) -> bool:
        """Step 2 API로 데이터 전송"""
        try:
            # API 타입 추가
            idea_with_type = idea.copy()
            idea_with_type['api_type'] = API_TYPE
            
            # 워크플로우 실행 요청
            url = f"{STEP2_API_URL}/workflows/create_contents/run"
            response = requests.post(url, json=idea_with_type, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Step 2 API 전송 성공: {result.get('message', 'Success')}")
                if result.get('job_id'):
                    logger.info(f"   작업 ID: {result['job_id']}")
                return True
            else:
                logger.error(f"❌ Step 2 API 응답 오류: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            logger.error("❌ Step 2 API 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
            return False
        except Exception as e:
            logger.error(f"❌ Step 2 API 전송 실패: {str(e)}")
            return False
    
    def process_idea(self, idea: Dict) -> bool:
        """단일 아이디어 처리"""
        try:
            idea_id = idea.get(COLUMN_ID)
            title = idea.get(COLUMN_TITLE_KO) or idea.get(COLUMN_TITLE_VI) or 'No Title'
            
            logger.info(f"📤 처리 중: ID={idea_id}, 제목={title}")
            
            # Step 2로 전송
            if self.send_to_step2(idea):
                # 성공 시 is_fetched 업데이트
                if self.update_is_fetched(idea_id):
                    self.processed_count += 1
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ 아이디어 처리 실패: {str(e)}")
            self.error_count += 1
            return False
    
    def check_step2_status(self) -> bool:
        """Step 2 API 서버 상태 확인"""
        try:
            response = requests.get(f"{STEP2_API_URL}/status", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def run(self):
        """메인 폴링 루프"""
        logger.info("=" * 60)
        logger.info("🚀 Supabase 폴링 서비스 시작")
        logger.info(f"📍 Supabase URL: {SUPABASE_URL}")
        logger.info(f"📡 Step 2 API: {STEP2_API_URL}")
        logger.info(f"⏱️  폴링 간격: {POLLING_INTERVAL}초")
        logger.info(f"📦 배치 크기: {BATCH_SIZE}개")
        logger.info(f"📂 로그 위치: {os.path.join(LOG_DIR, LOG_FILE)}")
        logger.info(f"⚙️  설정 파일: config_step1.ini")
        logger.info("=" * 60)
        
        # 로그 정리 주기 설정
        last_cleanup = datetime.now()
        
        # 초기 Step 2 상태 확인
        if not self.check_step2_status():
            logger.warning("⚠️  Step 2 API 서버가 오프라인 상태입니다.")
            logger.warning("   계속 진행하지만 데이터 전송은 실패할 수 있습니다.")
        
        while True:
            try:
                # 미처리 데이터 가져오기
                ideas = self.fetch_unfetched_ideas()
                
                if ideas:
                    # 각 아이디어 처리
                    for idea in ideas:
                        self.process_idea(idea)
                        time.sleep(0.5)
                    
                    logger.info(f"📊 통계: 처리됨={self.processed_count}, 오류={self.error_count}")
                else:
                    logger.debug("새로운 데이터가 없습니다.")
                
                # 하루에 한 번 로그 정리
                current_time = datetime.now()
                if (current_time - last_cleanup).days >= 1:
                    cleanup_old_logs()
                    last_cleanup = current_time
                    logger.info("🧹 로그 파일 정리 완료")
                
                # 다음 폴링까지 대기
                time.sleep(POLLING_INTERVAL)
                
            except KeyboardInterrupt:
                logger.info("\n⏹️  사용자가 서비스를 중지했습니다.")
                break
            except Exception as e:
                logger.error(f"❌ 예상치 못한 오류: {str(e)}")
                logger.info(f"⏳ {RETRY_DELAY}초 후 재시도...")
                time.sleep(RETRY_DELAY)
        
        logger.info(f"🏁 서비스 종료. 총 처리: {self.processed_count}개")

def main():
    """메인 함수"""
    try:
        poller = SupabasePoller()
        poller.run()
    except Exception as e:
        logger.error(f"❌ 서비스 시작 실패: {str(e)}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
