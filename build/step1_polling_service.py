#!/usr/bin/env python3
"""
Step 1: Supabase Polling Service (EXE 빌드용)
Supabase에서 데이터를 가져와 Step 2 API로 전송하는 폴링 서비스

빌드 방법:
pip install pyinstaller requests
pyinstaller --onefile --name "Step1_Supabase_Polling" step1_polling_service.py
"""

import json
import time
import requests
import logging
from datetime import datetime
import sys
import os
from typing import Dict, List, Optional

# ==================== 설정 변수 (여기만 수정하세요) ====================

# Supabase 설정
SUPABASE_URL = 'https://yenfccoefczqxckbizqa.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InllbmZjY29lZmN6cXhja2JpenFhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU5NDkyNzksImV4cCI6MjA2MTUyNTI3OX0.U1iQUOaNPSrEHf1w_ePqgYzJiRO6Bi48E2Np2hY0nCQ'

# 테이블 및 컬럼 설정
TABLE_NAME = 'contents_idea'
COLUMN_IS_FETCHED = 'is_fetched'
COLUMN_IS_AUTO_CREATED = 'is_auto_created'
COLUMN_ID = 'id'
COLUMN_TITLE_KO = 'title_ko'
COLUMN_TITLE_VI = 'title_vi'
COLUMN_SCENARIO = 'scenario'
COLUMN_COMPANY_ID = 'company_id'
COLUMN_STORE_ID = 'store_id'

# API 설정
STEP2_API_URL = 'http://localhost:5001'
API_TYPE = 'create_contents_on_user_idea'

# 폴링 설정
POLLING_INTERVAL = 30  # 초 단위
BATCH_SIZE = 1  # 한 번에 가져올 데이터 개수
RETRY_DELAY = 30  # API 오류 시 재시도 대기 시간

# 로그 설정
LOG_DIR = 'logs'  # 로그 디렉토리
LOG_FILE = 'step1_polling.log'
LOG_LEVEL = logging.INFO
LOG_RETENTION_DAYS = 1  # 로그 보관 일수

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
        '%(asctime)s - %(levelname)s - %(message)s',
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
        logger.info("=" * 60)
        
        # 로그 정리 주기 설정 (하루에 한 번)
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
                        time.sleep(0.5)  # 각 처리 사이 짧은 대기
                    
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
