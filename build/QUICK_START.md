# 🚀 워크플로우 자동화 빠른 시작 가이드

## 1️⃣ 첫 실행 체크리스트

### 필수 파일 확인
```
실행 폴더/
├── Step1_Supabase_Polling.exe  ✓
├── Step2_API_Server.exe         ✓
├── config_step1.ini             ✓ (설정 파일)
├── config_step2.ini             ✓ (설정 파일)
└── step3_workflows/             ✓ (워크플로우 폴더)
    └── create_contents/
        ├── main.py
        └── output/
```

### 설정 파일 수정 필요한 부분

#### config_step1.ini에서 반드시 수정:
```ini
[supabase]
url = 여기에_당신의_supabase_url_입력
key = 여기에_당신의_supabase_key_입력
```

#### config_step2.ini에서 확인:
```ini
[workflow]
base_path = ./step3_workflows  # 경로가 맞는지 확인
```

## 2️⃣ 실행 순서

1. **Step 2 먼저 실행** (API 서버)
   - `Step2_API_Server.exe` 더블클릭
   - "Workflow API Server Starting" 메시지 확인

2. **Step 1 실행** (Supabase 폴링)
   - `Step1_Supabase_Polling.exe` 더블클릭
   - "Supabase 폴링 서비스 시작" 메시지 확인

3. **정상 작동 확인**
   - 두 프로그램 모두 실행 중
   - 오류 메시지 없음
   - logs 폴더에 로그 파일 생성됨

## 3️⃣ 자주 발생하는 문제와 해결법

### 🔴 "Workflow not found" 오류
```ini
# config_step2.ini 수정
[workflow]
# 절대 경로로 변경
base_path = C:/Users/사용자명/Desktop/workflow/step3_workflows
```

### 🔴 "Connection refused" 오류
- Step 2가 실행 중인지 확인
- Windows 방화벽에서 포트 5001 허용

### 🔴 "설정 파일을 찾을 수 없습니다" 오류
- config_step1.ini와 config_step2.ini가 exe 파일과 같은 폴더에 있는지 확인

## 4️⃣ 테스트 방법

1. Supabase 대시보드에서 `contents_idea` 테이블에 테스트 데이터 추가:
   - `is_fetched`: false
   - `is_auto_created`: false
   - `title_ko`: "테스트 제목"

2. Step 1 콘솔에서 "새 데이터 발견" 메시지 확인

3. `step3_workflows/create_contents/output/` 폴더에 결과 파일 생성 확인

## 5️⃣ 로그 확인

- Step 1 로그: `logs/step1_polling.log`
- Step 2 로그: `logs/step2_api_server.log`
- 워크플로우 로그: `step3_workflows/create_contents/logs/workflow.log`

## 6️⃣ 설정 변경 시

1. 해당 ini 파일 수정
2. 프로그램 종료 (Ctrl+C 또는 창 닫기)
3. 프로그램 다시 실행

## 7️⃣ 자동 시작 설정 (선택사항)

Windows 시작 시 자동 실행하려면:
1. Win+R → `shell:startup`
2. 두 exe 파일의 바로가기 만들기
3. Step2 바로가기 이름을 "1_Step2_API_Server"로 변경 (먼저 실행되도록)

---

💡 **도움말**: 
- 로그 파일은 매일 자동 삭제됩니다
- 폴링 간격을 늘리려면 config_step1.ini의 interval_seconds 수정
- 새 워크플로우 추가는 workflow_templates 폴더 참고

📧 **문제가 계속되면**:
- 로그 파일 내용 확인
- 설정 파일 경로 재확인
- Supabase 연결 정보 확인
