# 🔧 Windows 경로 설정 가이드

## 현재 설정 상태

### ✅ 이미 설정된 항목들:
- Supabase URL과 API Key
- 테이블명과 컬럼명
- 폴링 간격 (10초)
- API 타입과 워크플로우 매핑

### ⚠️ Windows에서 수정 필요한 항목:
**config_step2.ini 파일의 [workflow] 섹션만 수정하면 됩니다!**

```ini
[workflow]
base_path = ./step3_workflows  # <- 이 부분만 수정
```

## 📍 Windows 경로 설정 방법

### 1. exe 파일을 실행할 폴더 구조 확인
```
C:/Users/사용자명/Desktop/workflow/  (예시)
├── Step1_Supabase_Polling.exe
├── Step2_API_Server.exe
├── config_step1.ini
├── config_step2.ini
└── step3_workflows/
    └── create_contents/
        ├── main.py
        └── output/
```

### 2. 다음 중 하나를 선택:

#### 옵션 A: 상대 경로 사용 (권장)
```ini
base_path = ./step3_workflows
```
- exe 파일과 같은 폴더에 step3_workflows 폴더가 있을 때

#### 옵션 B: 절대 경로 사용
```ini
base_path = C:/Users/사용자명/Desktop/workflow/step3_workflows
```
- 정확한 전체 경로 지정
- 사용자명 부분을 실제 Windows 사용자명으로 변경

### 3. 경로 확인 방법
1. Windows 탐색기에서 step3_workflows 폴더 찾기
2. 주소창 클릭
3. 전체 경로 복사
4. config_step2.ini에 붙여넣기

## 🚨 자주 하는 실수

### ❌ 잘못된 경로 예시:
```ini
base_path = step3_workflows          # ./ 빠짐
base_path = .\step3_workflows        # 역슬래시 사용
base_path = "../step3_workflows"     # 따옴표 사용
```

### ✅ 올바른 경로 예시:
```ini
base_path = ./step3_workflows
base_path = C:/workflow/step3_workflows
base_path = D:/projects/automation/step3_workflows
```

## 💡 팁

1. **먼저 상대 경로로 시도**: `./step3_workflows`
2. **안 되면 절대 경로로 변경**: 전체 경로 입력
3. **경로에 한글 피하기**: 가능하면 영문 경로 사용
4. **공백 있는 경로 피하기**: `Program Files` 같은 폴더 피하기

---

**준비 완료!** Windows 경로만 알려주시면 config_step2.ini를 수정해드리겠습니다.
