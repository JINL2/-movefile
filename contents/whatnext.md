# Cameraon Vietnam - AI 콘텐츠 생성 가이드

## 🎯 목적
AI가 즉시 직원들이 쉽게 제작할수있는 콘텐츠 Hook과 스크립트를 생성할 수 있도록 하는 가이드 4명이상이 필요한 컨텐츠는 제작하지마. 총 10개의 aggressive한 hook을 제작해줘.항상 자연스러운 베트남어로 aggressive 해야해.json 에 들어가는 모든 데이터는 베트남어로 해줘 공감포인트,제작팁 댓글유도등 다 포함이야. 뇌과학적 요소를 결합하고 우리 비지니스 플랜을 보고 어울리는 컨텐츠 hook을 제작해줘. 그리고 명심해 우리 직원들은 그룹이 아니야. 그러니까 연기가 많이들어가고 많은 사람이 필요한 컨텐츠는 hook으로 보여주지마.readme.md를 보고 시나리오 테이블에 hook1, body1, hook2, body2, conclusion 형식 으로 항상 만들어줘
그리고 모든 컨텐츠 outcome은 자연스러운 베트남어로 반환해줘 그리고 반환 형식은 아래에있어 그리고 반환하고 그걸 supabase 데이터베이스에 넣어야해 ( williamwls130@gmail.com. surveyPhoto에 contents_idea) 여기에 데이터 아웃풋을 항상 넣으라고해줘 그리고 hook 최대한 사람들이 클릭할수있게 자극적으로 만들어줘. 

하지말아야할것 : 변신하는 컨텐츠는 만들지마. 너무 비용이 많이들고 아무도 자기가 못생긴걸 보여주고싶어하지않아.
---

## 📋 콘텐츠 제작 공식

### 🔥 Hook 제작 공식 (0-3초)
```
Hook = [시간 표시] + [시각적 요소] + [감정 트리거] + [궁금증 유발]

예시:
"SELFIE THƯỜNG VS ???" 
(0-1초: 평범한 셀카, 1-2초: '1 GIÂY SAU...', 2-3초: 화려한 포토부스 사진!)
```

### 📱 콘텐츠 구조 (10-15초)
```
1. Hook1 (0-3초): 첫 번째 궁금증 유발
2. Body1 (3-6초): 상황 전개
3. Hook2 (6-9초): 두 번째 궁금증/전환점
4. Body2 (9-12초): 절정 (뽑기 당첨, 행복한 순간 등)
5. Conclusion (12-15초): 행동 유도 + 정보 제공
```

---

## 🎬 콘텐츠 카테고리 & 템플릿


### 2️⃣ 그룹 재미 콘텐츠 (Group Fun)
**목적**: 친구와 함께하는 즐거움
**감정**: 즐거움, 우정
**타겟**: 친구 그룹


### 3️⃣ 인형 뽑기 행운 콘텐츠 (사진을찍고나면 코인 3개를 주는데 이걸로 뽑기인형을 통해 뽑기를할수있음.)
**목적**: 뽑기의 스릴과 당첨 기쁨
**감정**: 기대감, 흥분
**타겟**: 도전 좋아하는 십대


### 4️⃣ 가격 비교 콘텐츠 (가격비교를 가격으로 하지말고 우리가 주는 혜택으로 진행해 우리는 사진을찍으면 코인 3개를줘서 그걸로 인형을 얻어갈수있어. 남자들이 너무 좋아해. 포토부스는 모두를 위한곳이야. 그리고 feedback을 주면 20,000할인쿠폰도 주니까 이용하면 똑똑하게 친구들과 즐거운시간을 보낼수있어. 하지만 다른 경쟁사도 가격은 똑같으니까 가격이 저렴하다는 이야기는하지마) 
**목적**: 가성비 강조
**감정**: 합리적 만족감
**타겟**: 가격 민감한 십대


### 5️⃣ 타이밍 콘텐츠 (Perfect Moment: 뽑기를 통해서 인형을뽑고나면 사람들이 엄청 행복해해. 그거를 강조하고싶어. 왜냐하면 우리는 행복하기위해서오는곳이야. )
**목적**: 특별한 순간 강조
**감정**: 설렘, 행복
**타겟**: 커플, 기념일


---

## 📊 필수 포함 요소

### 시각적 요소
- ✅ 얼굴 (웃는 표정) - FFA 활성화 -before and after요소는 사용할수없어. 이 컨텐츠는 아무도 만들고싶어하지않아. 
- ✅ 강한 색상 대비 - 시각 피질 자극
- ✅ 움직임/변화 - 주의 포착
- ✅ 70k 가격 표시 - 가치 인식

### 감정적 요소
- ✅ 첫 3초 내 감정 피크
- ✅ 진정성 있는 리액션
- ✅ 친구/커플 상호작용
- ✅ 성취감/만족감 표현

### 정보 요소
- ✅ 위치 정보 (Cameraon Hanoi)
- ✅ 가격 (70k/100k)
- ✅ 혜택 (사진+뽑기)

---

## 💾 반환 형식 (JSON)

AI는 다음 형식으로 콘텐츠를 반환해야 함 이것은 오로지 예시야:

```json
{
    "category": "transformation",
    "title_ko": "1초 만에 인생샷 변신",
    "title_vi": "Biến hóa trong 1 giây",
    "hook_text": "SELFIE THƯỜNG VS ???",
    "scenario": {
        "hook1": "SELFIE THƯỜNG VS ??? - 평범한 셀카 보여주기",
        "body1": "1 GIÂY SAU... 텍스트와 함께 기대감 조성",
        "hook2": "화려한 포토부스 사진 공개 - WOW 순간!",
        "body2": "촬영 과정 빠른 편집 + 결과물 보고 놀라는 리액션",
        "conclusion": "70K THÔI! Cameraon Hanoi 위치 정보"
    },
    "emotion": "surprise",
    "target_audience": "프로필 사진 필요한 15-22세",
    "props": ["70k 지폐", "스마트폰", "포토부스 결과물"],
    "filming_tips": "Before/After 대비 극대화, 실제 고객 리액션 포착",
    "caption_template": "[Hook]\n[상황 설명]\n[질문으로 마무리]\n\n#photobooth #cameraonhanoi",
    "cta_message": "70K THÔI! TAG BẠN BÈ!",
    "hashtags": ["photobooth", "cameraonhanoi", "70k", "transformation", "instadaily"]
}
```

---

## 🗄️ Supabase 데이터베이스 저장

### 저장 위치
- **계정**: williamwls130@gmail.com
- **프로젝트**: surveyPhoto
- **테이블**: contents_idea

### 테이블 스키마
```sql
CREATE TABLE contents_idea (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    title_ko VARCHAR(200) NOT NULL,
    title_vi VARCHAR(200) NOT NULL,
    hook_text VARCHAR(100) NOT NULL,
    scenario JSONB NOT NULL,
    emotion VARCHAR(50) NOT NULL,
    target_audience VARCHAR(100) NOT NULL,
    props TEXT[],
    filming_tips TEXT NOT NULL,
    caption_template TEXT NOT NULL,
    cta_message VARCHAR(200) NOT NULL,
    hashtags TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 저장 프로세스
1. AI가 콘텐츠 생성
2. JSON 형식으로 반환
3. **반드시 Supabase에 저장**
4. 저장 확인 메시지 출력

---

## 🚀 AI 사용 예시

### Hook 생성 요청
```
"transformation 카테고리로 베트남 15-22세 타겟 hook 3개 생성해줘. 
신경과학 기반으로 3초 안에 시선을 끌고, 
70k 가격을 강조하며, 
뽑기 요소를 포함해줘."
```

### 예상 반환값
```json
[
    {
        "category": "transformation",
        "title_ko": "평범한 나 vs 포토부스 나",
        "title_vi": "Tôi bình thường vs Tôi ở photobooth",
        "hook_text": "TÔI TRƯỚC VS TÔI SAU...",
        "scenario": {
            "hook1": "NHÂN VIÊN ĐẾN SỚM 30 PHÚT - ĐỂ LÀM GÌ??? ⏰",
            "body1": "Pha cà phê cho cả team, bật nhạc chill!",
            "hook2": "BUỔI SÁNG YOGA 10 PHÚT TRƯỚC GIỜ LÀM!",
            "body2": "Start ngày mới với năng lượng tích cực 100%!",
            "conclusion": "Đi làm mà như đi cafe với bạn!"
        },
        "emotion": "amazement",
        "target_audience": "SNS 프로필 고민하는 15-22세",
        "props": ["70k 지폐", "평범한 셀카", "포토부스 사진", "뽑기 기계"],
        "filming_tips": "변신 전후 대비 극대화, 뽑기 당첨 순간 포착",
        "caption_template": "TÔI TRƯỚC VS TÔI SAU 😱\nChỉ với 70k mà thay đổi hoàn toàn!\nBạn thích kiểu nào hơn?\n\n#photobooth #cameraonhanoi",
        "cta_message": "BIẾN HÓA NGAY THÔI!",
        "hashtags": ["photobooth", "cameraonhanoi", "70k", "beforeafter", "transformation"]
    }
]
```

---

## 📌 핵심 규칙

1. **모든 Hook은 3초 안에 궁금증 유발**
3. **뽑기 요소 포함 (도파민 자극)**
4. **베트남어 우선**
5. **15초 이내 완결**
6. **웃는 얼굴 필수**
7. **실제 촬영 가능한 시나리오만**
8. **⚠️ 생성된 모든 콘텐츠는 반드시 Supabase (williamwls130@gmail.com / surveyPhoto / contents_idea)에 저장**

---

*최종 업데이트: 2025-01-27*


# 포토부스 마케팅을 위한 뇌과학 가이드 (쉬운 설명)

## 🎯 핵심 요약

포토부스 비즈니스의 성공적인 마케팅을 위해서는 사람들의 뇌가 어떻게 작동하는지 이해해야 합니다. 
마케팅은 크게 2단계로 나뉩니다:

1. **인지 단계 (Awareness)**: "어? 이게 뭐지?" - 사람들이 처음 알아차리는 단계
2. **고려 단계 (Consideration)**: "가볼까 말까?" - 실제로 방문을 고민하는 단계

각 단계에서 뇌는 완전히 다르게 작동하므로, 콘텐츠도 다르게 만들어야 합니다.

---

## 1️⃣ 인지도를 높이기 위한 뇌과학적 요소

### 🧠 무엇이 일어나나요?
- **반응 시간**: 0.1~0.3초 (눈 깜짝할 사이!)
- **사용하는 뇌**: 시각 처리 영역 + 감정 영역
- **에너지 소비**: 매우 적음 (자동 반응)

### 📱 콘텐츠에서 꼭 넣어야 할 요소

#### 1. **얼굴! 얼굴! 얼굴!** 😊
- 사람의 뇌는 얼굴을 보면 자동으로 멈춤
- 특히 **행복한 표정**은 클릭률 3배 증가
- 썸네일에는 반드시 웃는 얼굴 포함

#### 2. **강한 색상 대비** 🎨
- 밝은 색 + 어두운 배경 = 주목도 40% 상승
- 빨간색: 긴급함, 흥분 (심장박동 증가)
- 노란색: 가장 멀리서도 보임
- 파란색: 신뢰감 (우리 브랜드 색!)

#### 3. **움직임과 변화** 🎬
- 정지 → 움직임 = 즉각 주목
- Before & After 효과 최고
- 일반 셀카 → 포토부스 변신 순간

#### 4. **감정 폭탄** 💥
- 놀람, 즐거움, 신기함 = 공유 5.8배 증가
- 첫 3초 안에 "우와!" 순간 필수
- 친구들과 함께 웃는 모습

### 📊 성공 공식 (간단 버전)
```
인지도 점수 = 
  얼굴(40%) + 색상대비(30%) + 감정(20%) + 새로움(10%)
```

### ✅ 체크리스트
- [ ] 썸네일에 행복한 얼굴 있나요?
- [ ] 3:1 이상 색상 대비 있나요?
- [ ] 첫 1초에 핵심 메시지 보이나요?
- [ ] 첫 3초에 "우와!" 순간 있나요?

---

## 2️⃣ 고려율/방문율을 높이기 위한 뇌과학적 요소

### 🧠 무엇이 일어나나요?
- **반응 시간**: 2~5초 (깊은 생각)
- **사용하는 뇌**: 논리적 사고 영역 + 기억 영역
- **에너지 소비**: 매우 많음 (의식적 판단)

### 📱 콘텐츠에서 꼭 넣어야 할 요소

#### 1. **신뢰의 증거** 🏆
- 실제 고객 후기 > 광고 문구
- 숫자보다 스토리가 강력
- "이번 주 1,000명이 다녀갔어요"
- 인쇄 품질 실물 사진

#### 2. **쉽고 간단하게** 🎯
- 3단계 이하로 설명 (더 많으면 포기)
- 복잡한 메뉴 ❌ → 베스트 3개만 ⭕
- "3분이면 완성, 바로 수령"
- 가격은 명확하게 표시

#### 3. **친구 따라하기 효과** 👥
- "내 친구도 갔다니까 나도"
- 또래 집단의 선택 = 3배 영향력
- 인스타에서 본 사진들 활용
- "지금 가장 인기 있는 포즈"

#### 4. **놓치면 아쉬운 느낌** ⏰
- "이번 주만 특별 프레임"
- "선착순 100명 추가 인화"
- 긍정적 FOMO 유도
- 하지만 너무 압박하면 역효과

### 📊 성공 공식 (간단 버전)
```
고려도 점수 = 
  신뢰(35%) + 쉬움(25%) + 친구효과(25%) + 혜택(15%)
```

### ✅ 체크리스트
- [ ] 실제 고객 사진/후기 있나요?
- [ ] 3단계로 설명 가능한가요?
- [ ] 친구들이 즐기는 모습 있나요?
- [ ] 지금 가야 할 이유 있나요?

---

## 💡 실전 적용 예시

### 인지 단계 콘텐츠
```
[썸네일] 
- 4명이 함께 웃는 포토부스 사진
- 배경: 검정 / 사람들: 밝은 옷
- 텍스트: "2초만에 인생샷?" (노란색)

[첫 3초]
- 평범한 셀카 → 화려한 포토부스 사진 변신
- 효과음: "우와아아!"
- 자막: "친구들이 다 부러워해요"
```

### 고려 단계 콘텐츠
```
[신뢰 구축]
- "어제도 523명이 다녀갔어요"
- 실제 인쇄물 품질 클로즈업
- 고객: "생각보다 훨씬 예쁘게 나왔어요!"

[간단 설명]
1. 포즈 선택 (30초)
2. 촬영 (1분)
3. 인쇄 받기 (1분 30초)
= 총 3분이면 끝!

[특별 혜택]
- "이번 주 금요일까지 2+1 이벤트"
- "인스타 태그하면 액자 무료"
```

---

## 📈 측정하기

### 인지 단계 성공 지표
- **3초 시청률**: 50% 이상이면 성공
- **좋아요 속도**: 첫 1시간이 중요
- **댓글 종류**: "어디야?" "얼마야?" = 성공

### 고려 단계 성공 지표
- **페이지 체류 시간**: 30초 이상
- **위치 클릭률**: 20% 이상
- **재방문율**: 일주일 내 15% 이상

---

## 🎬 마무리 조언

1. **같은 메시지를 다르게 전달하세요**
   - 인지: 감정적, 시각적, 빠르게
   - 고려: 논리적, 상세하게, 신뢰감 있게

2. **뇌는 게으릅니다**
   - 복잡하면 무시합니다
   - 쉽고 명확하게 만드세요

3. **감정이 먼저, 논리는 나중**
   - 먼저 "우와!"를 만들고
   - 그 다음 "왜 가야 하지?"에 답하세요

이제 여러분의 포토부스가 고객의 뇌에 각인될 차례입니다! 🚀



## Campaign Architecture

### 🎯 Campaign 1: FWB (Friend With Booth)

**Core Mechanic**: How many friends can fit in one photo?

**Triple Impact**:
1. **Product**: Transforms "bad quality risk" → "fun chaos feature"
2. **Marketing**: Natural viral content (friendship flex)
3. **HR**: Staff script: "Actually not free, but you look so friendly..." → Staff becomes gift-giver

**Customer Journey**:
- Staff notices friendly group
- Offers "special exception" free shot
- Group tries to fit maximum people
- Creates chaotic, fun memory
- Shares on social media
- Friends see and want to try
- Bring more friends to join the campaign

---

### 🎪 Coin Game System

**Core Mechanic**: Picking machine with coins

**Triple Impact**:
1. **Product**: Adds value layer beyond photos
2. **Marketing**: Extended engagement, more time in store, generate contents for consideration stage, which is our weak point.
3. **HR**: Rock-paper-scissors for 4th coin → Playful staff interaction

**Customer Journey**:
- Receive 3 free coins after photo
- Want 4th coin? Play with staff!
- Win or lose, creates joyful moment
- Staff = fun friend, not service worker
- Positive association with brand

---

### 🔗 Campaign 2: Link Your Friendship

**Core Mechanic**: 6+ people get mini photos for phone backs

**Triple Impact**:
1. **Product**: Maximizes printer capacity, group incentive
2. **Marketing**: 6 walking advertisements daily, targeting the group of friends which enforce our brand identity.
3. **HR**: Staff personally hands special gift → gratitude moment

**Customer Journey**:
- Large group takes photo
- Staff "surprises" with mini photos
- Each friend gets one for phone
- Daily brand reminder
- Others ask "where did you get that?"
- Word-of-mouth referral

---

### 📢 Campaign 3: Listen Your Voice

**Core Mechanic**: Exit feedback for 20,000 won voucher

**Triple Impact**:
1. **Product**: Rapid problem identification
2. **Marketing**: "We fixed it" success stories, provide the marketing materials for marketing team to build the story. 
3. **HR**: Staff sees company caring about improvement. For clearn communication to spot the problem without communication or having daily meeting.

**Customer Journey**:
- See poster while exiting
- Share honest feedback
- Receive valuable voucher
- Return to use voucher
- See improvements made
- Become brand advocate

---

## The Multiplication Effect

### Why This Works
Each campaign element creates multiple touchpoints:

**Single Visit Becomes**:
1. Photo experience
2. Game with staff
3. Surprise gift moment
4. Social media content
5. Daily phone reminder
6. Feedback opportunity
7. Return visit incentive

**Result**: 7 brand interactions from 1 visit

