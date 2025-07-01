# 워크플로우 자동화 EXE 빌드 가이드

## 📋 빌드 전 준비사항

1. **Python 설치** (3.8 이상)
   - https://www.python.org/ 에서 다운로드
   - 설치 시 "Add Python to PATH" 체크 필수

2. **필요한 패키지 설치**
   ```cmd
   pip install pyinstaller requests flask flask-cors
   ```

## 🛠️ 빌드 방법

### 방법 1: 자동 빌드 (추천)
1. `build` 폴더로 이동
2. `build_windows.bat` 더블클릭
3. `dist` 폴더에 exe 파일 생성됨

### 방법 2: 수동 빌드
```cmd
# Step 1 빌드
pyinstaller --onefile --name "Step1_Supabase_Polling" step1_polling_service.py

# Step 2 빌드
pyinstaller --onefile --name "Step2_API_Server" --hidden-import=flask --hidden-import=flask_cors step2_api_server.py
```

## 📂 폴더 구조

빌드 후:
```
build/
├── step1_polling_service.py    # Step 1 소스코드
├── step2_api_server.py         # Step 2 소스코드
├── build_windows.bat           # 빌드 스크립트
├── dist/                       # 빌드된 EXE 파일
│   ├── Step1_Supabase_Polling.exe
│   └── Step2_API_Server.exe
└── step3_workflows/            # 워크플로우 폴더 (복사 필요)
```

## ⚙️ 설정 변경

각 Python 파일 상단의 설정 변수 섹션에서 수정:

### Step 1 설정 (step1_polling_service.py)
```python
# Supabase 설정
SUPABASE_URL = 'your-supabase-url'
SUPABASE_KEY = 'your-supabase-key'

# 테이블 설정
TABLE_NAME = 'contents_idea'
COLUMN_IS_FETCHED = 'is_fetched'

# 폴링 설정
POLLING_INTERVAL = 10  # 초
```

### Step 2 설정 (step2_api_server.py)
```python
# 서버 설정
SERVER_PORT = 5001

# 워크플로우 경로
WORKFLOW_BASE_PATH = '../step3_workflows'
```

## 🚀 실행 방법

1. **Step 2 서버 먼저 실행**
   - `Step2_API_Server.exe` 더블클릭
   - 콘솔창에 "Workflow API Server Starting" 확인

2. **Step 1 폴링 서비스 실행**
   - `Step1_Supabase_Polling.exe` 더블클릭
   - 콘솔창에 "Supabase 폴링 서비스 시작" 확인

3. **워크플로우 폴더 준비**
   - exe 파일과 같은 위치에 `step3_workflows` 폴더 복사
   - 폴더 구조:
     ```
     실행파일위치/
     ├── Step1_Supabase_Polling.exe
     ├── Step2_API_Server.exe
     └── step3_workflows/
         └── create_contents/
             ├── main.py
             └── output/
     ```

## 🔧 문제 해결

### "Python이 설치되지 않았습니다" 오류
- Python 설치 후 시스템 재시작
- 명령 프롬프트에서 `python --version` 확인

### "모듈을 찾을 수 없습니다" 오류
```cmd
pip install --upgrade pip
pip install pyinstaller requests flask flask-cors
```

### exe 실행 시 바로 꺼지는 경우
- 명령 프롬프트에서 실행하여 오류 메시지 확인:
  ```cmd
  cd dist
  Step2_API_Server.exe
  ```

### 워크플로우를 찾을 수 없다는 오류
- `step3_workflows` 폴더가 exe 파일과 같은 위치에 있는지 확인
- 폴더 내부에 워크플로우 폴더들이 있는지 확인

## 📂 폴더 구조 예시

실행 후 생성되는 폴더 구조:
```
실행파일위치/
├── Step1_Supabase_Polling.exe
├── Step2_API_Server.exe
├── logs/                      # 로그 폴더 (자동 생성)
│   ├── step1_polling.log
│   └── step2_api_server.log
└── step3_workflows/
    └── create_contents/
        ├── main.py
        ├── output/            # 결과 파일
        └── logs/              # 워크플로우 로그
            └── workflow.log
```

## 🔄 자동 시작 설정

### Windows 작업 스케줄러 사용
1. 작업 스케줄러 열기 (taskschd.msc)
2. "기본 작업 만들기" 클릭
3. 트리거: "컴퓨터 시작 시"
4. 동작: 프로그램 시작
5. 프로그램 경로: exe 파일 선택
6. Step2를 먼저, Step1을 나중에 실행하도록 설정

### 시작 프로그램에 추가
1. Win + R → `shell:startup`
2. 바로가기 생성:
   - Step2_API_Server.exe 바로가기
   - Step1_Supabase_Polling.exe 바로가기

## 📝 로그 관리

### 로그 파일 위치
모든 로그는 `logs/` 폴더에 저장됩니다:
- `logs/step1_polling.log` - Step 1 실행 로그
- `logs/step2_api_server.log` - Step 2 실행 로그
- `step3_workflows/create_contents/logs/workflow.log` - 워크플로우 실행 로그

### 로그 자동 정리
- 하루에 한 번 자동으로 오래된 로그 파일 삭제
- 기본 보관 기간: 1일
- 설정 변경: `LOG_RETENTION_DAYS` 변수 수정

### 로그 형식
```
2025-01-01 10:30:45 - INFO - ✅ 데이터 처리 완료
2025-01-01 10:30:46 - ERROR - ❌ 연결 오류 발생
```

## 🛡️ 보안 주의사항

1. **API 키 보호**
   - 소스코드의 API 키는 환경변수나 별도 설정 파일로 분리 권장
   - exe 파일 배포 시 주의

2. **네트워크 보안**
   - Step 2 서버는 localhost에서만 실행 (기본값)
   - 외부 접근이 필요한 경우 방화벽 설정 필요

## 📌 참고사항

- exe 파일은 단독 실행 가능 (Python 설치 불필요)
- 워크플로우 수정은 step3_workflows 폴더 내용만 변경
- 설정 변경 시 재빌드 필요
