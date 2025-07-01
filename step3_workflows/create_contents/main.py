#!/usr/bin/env python3
"""
Create Contents Workflow - 간단한 테스트 버전
받은 JSON 데이터를 텍스트 파일로 저장
"""

import json
import os
import logging
from datetime import datetime
from pathlib import Path

# 로그 설정
LOG_DIR = 'logs'
LOG_FILE = 'workflow.log'
LOG_RETENTION_DAYS = 1

# 로그 디렉토리 생성
def create_log_directory():
    log_path = Path(__file__).parent / LOG_DIR
    if not log_path.exists():
        log_path.mkdir(exist_ok=True)

# 오래된 로그 정리
def cleanup_old_logs():
    try:
        log_path = Path(__file__).parent / LOG_DIR / LOG_FILE
        if log_path.exists():
            file_modified_time = datetime.fromtimestamp(log_path.stat().st_mtime)
            current_time = datetime.now()
            
            if (current_time - file_modified_time).days >= LOG_RETENTION_DAYS:
                log_path.unlink()
                print(f"Old log file deleted: {log_path}")
    except Exception as e:
        print(f"Error cleaning up logs: {e}")

# 로깅 설정
def setup_logging():
    create_log_directory()
    cleanup_old_logs()
    
    log_path = Path(__file__).parent / LOG_DIR / LOG_FILE
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def main():
    """메인 워크플로우 실행"""
    try:
        # 현재 디렉토리 설정
        workflow_dir = Path(__file__).parent
        data_file = workflow_dir / "_data.json"
        output_dir = workflow_dir / "output"
        
        # output 디렉토리 생성
        output_dir.mkdir(exist_ok=True)
        
        # 입력 데이터 읽기
        if data_file.exists():
            with open(data_file, 'r', encoding='utf-8') as f:
                input_data = json.load(f)
            
            logger.info("✅ 입력 데이터 로드 완료")
            logger.info(f"📋 데이터 ID: {input_data.get('id', 'N/A')}")
            
            # 타임스탬프 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 출력 파일명 생성
            idea_id = input_data.get('id', 'unknown')
            output_filename = f"content_{idea_id}_{timestamp}.txt"
            output_path = output_dir / output_filename
            
            # 텍스트 파일로 저장
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write(f"WORKFLOW: Create Contents from User Idea\n")
                f.write(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                f.write("📥 받은 데이터 (JSON):\n")
                f.write("-" * 80 + "\n")
                f.write(json.dumps(input_data, ensure_ascii=False, indent=2))
                f.write("\n\n")
                
                # 주요 필드 추출
                f.write("📋 주요 정보:\n")
                f.write("-" * 80 + "\n")
                f.write(f"ID: {input_data.get('id', 'N/A')}\n")
                f.write(f"베트남어 제목: {input_data.get('title_vi', 'N/A')}\n")
                f.write(f"한국어 제목: {input_data.get('title_ko', 'N/A')}\n")
                f.write(f"회사 ID: {input_data.get('company_id', 'N/A')}\n")
                f.write(f"매장 ID: {input_data.get('store_id', 'N/A')}\n")
                f.write(f"API 타입: {input_data.get('api_type', 'N/A')}\n")
                f.write("\n")
                
                # 시나리오 정보
                scenario = input_data.get('scenario', {})
                if scenario:
                    f.write("📝 시나리오:\n")
                    f.write("-" * 80 + "\n")
                    f.write(f"Hook 1: {scenario.get('hook1', 'N/A')}\n")
                    f.write(f"Body 1: {scenario.get('body1', 'N/A')}\n")
                    f.write(f"Hook 2: {scenario.get('hook2', 'N/A')}\n")
                    f.write(f"Body 2: {scenario.get('body2', 'N/A')}\n")
                    f.write(f"Conclusion: {scenario.get('conclusion', 'N/A')}\n")
                    f.write("\n")
                
                f.write("=" * 80 + "\n")
                f.write("✅ 워크플로우 완료!\n")
                f.write(f"💾 저장 위치: {output_filename}\n")
            
            # 결과 반환
            result = {
                "status": "completed",
                "message": "JSON 데이터를 텍스트 파일로 저장했습니다",
                "output_file": output_filename,
                "output_path": str(output_path),
                "processed_at": datetime.now().isoformat()
            }
            
            logger.info(f"✅ 워크플로우 완료: {output_filename}")
            
            # 결과를 JSON으로 출력 (python_server.py가 파싱할 수 있도록)
            print(json.dumps(result, ensure_ascii=False))
            
            return result
            
        else:
            error_result = {
                "status": "error",
                "message": "_data.json 파일을 찾을 수 없습니다"
            }
            logger.error("_data.json 파일을 찾을 수 없습니다")
            print(json.dumps(error_result, ensure_ascii=False))
            return error_result
            
    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"오류 발생: {str(e)}"
        }
        logger.error(f"워크플로우 오류: {str(e)}")
        print(json.dumps(error_result, ensure_ascii=False))
        return error_result

if __name__ == "__main__":
    main()
