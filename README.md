# 🎓 EduCoach AI - 영어 독해 평가 시스템

고정 지문으로 사용자의 영어 독해, 문법, 어휘를 평가하고 맞춤 학습 방법을 추천하는 AI 서비스

## 📖 평가 지문

**Passage:**

```
Many people believe that success is only about talent or luck, but in reality, 
persistence plays a much bigger role. History shows countless examples of 
individuals who failed many times before achieving their goals. For instance, 
Thomas Edison tested thousands of materials before inventing the light bulb. 
His determination proved that consistent effort can lead to remarkable results.

In modern society, persistence is still essential. Students who continue studying 
even after facing difficulties often perform better than those who give up quickly. 
Similarly, athletes train for years to improve their skills, even when progress 
seems slow. These examples remind us that success is not a single event but a 
journey that requires patience and hard work.
```

**평가 질문 (3개):**

1. What is the main idea of this passage?
2. Give an example from the passage that supports the importance of persistence.
3. In your own words, explain why persistence is important in modern society.

## 📁 프로젝트 구조

```
educoach-ai/
├── agents/
│   ├── evaluation_agent.py      # 평가 (독해/문법/어휘)
│   ├── diagnosis_agent.py       # 진단 (수준 판정)
│   └── recommendation_agent.py  # 학습 추천
├── api/
│   └── main.py                  # FastAPI 서버
├── .env                         # 환경 변수 (API 키)
├── requirements.txt             # 패키지 목록
└── README.md
```

## 🚀 설치 및 실행

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일 생성:

```bash
ANTHROPIC_API_KEY=your_actual_api_key
```

### 3. 서버 실행

```bash
uvicorn api.main:app --reload
```

서버 주소: `http://127.0.0.1:8000`

## 📖 API 사용법

### 방법 1: Swagger UI 사용 (추천)

1. 브라우저에서 `http://127.0.0.1:8000/docs` 열기
2. **GET /passage** 실행하여 지문 확인
   ```json
   {
     "passage": "Many people believe...",
     "questions": [...]
   }
   ```
3. **POST /evaluate** 에서 답변 제출
   ```json
   {
     "answers": [
       "The main idea is that persistence is more important than talent.",
       "Thomas Edison tested thousands of materials before inventing the light bulb.",
       "Persistence helps students and athletes achieve their goals through consistent effort."
     ]
   }
   ```

### 방법 2: cURL 사용

#### 지문 가져오기

```bash
curl http://127.0.0.1:8000/passage
```

#### 답변 평가하기

```bash
curl -X POST http://127.0.0.1:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "answers": [
      "The main idea is that persistence is more important than talent.",
      "Thomas Edison tested thousands of materials.",
      "Persistence helps students overcome difficulties."
    ]
  }'
```

## 📊 응답 예시

```json
{
  "scores": {
    "reading_comprehension": 85,
    "grammar": 70,
    "vocabulary": 75,
    "feedback": "지문의 주제를 잘 이해했습니다. 문법은 기본적으로 정확하나 복잡한 문장 구조 연습이 필요합니다."
  },
  "diagnosis": {
    "level": "intermediate",
    "weakness": ["문법"],
    "diagnosis_summary": "문법 영역에서 보완이 필요합니다."
  },
  "recommendations": {
    "level_advice": "중급 학습자를 위한 추천입니다.",
    "weakness_recommendations": [
      "복잡한 문장 구조 학습 (관계대명사, 접속사)",
      "영작 연습으로 문법 적용력 키우기",
      "온라인 문법 퀴즈 풀기"
    ],
    "general_tips": [
      "실전 영어 사용 기회를 늘리세요",
      "영어 일기 쓰기 도전",
      "온라인 언어 교환 파트너 찾기"
    ]
  }
}
```

## 🎯 평가 기준

### 점수 범위 (0-100)

* **독해 (Reading Comprehension)** : 지문 이해도, 주제 파악, 세부 내용 이해
* **문법 (Grammar)** : 문장 구조, 시제, 품사 사용
* **어휘 (Vocabulary)** : 단어 선택, 어휘 다양성, 고급 어휘 사용

### 수준 판정

| 평균 점수 | 수준         | 설명           |
| --------- | ------------ | -------------- |
| 0-59      | Beginner     | 기초 학습 필요 |
| 60-79     | Intermediate | 중급 학습자    |
| 80-100    | Advanced     | 고급 학습자    |

## 🔧 트러블슈팅

### 1. API 키 오류

```
Error: API key not found
```

**해결:** `.env` 파일에 올바른 API 키 입력 확인

### 2. 모듈을 찾을 수 없음

```
ModuleNotFoundError: No module named 'agents'
```

**해결:** 프로젝트 루트 디렉토리에서 실행

```bash
uvicorn api.main:app --reload
```

### 3. 답변 개수 오류

```
400 Bad Request: 3개의 질문에 대한 답변이 필요합니다
```

**해결:** 반드시 3개의 답변을 배열로 전달

## 🌐 프론트엔드 연동 예시

```javascript
// 1. 지문 가져오기
const passageResponse = await fetch('http://127.0.0.1:8000/passage');
const { passage, questions } = await passageResponse.json();

// 2. 사용자 답변 수집 후 평가
const answers = [
  userAnswer1,
  userAnswer2,
  userAnswer3
];

const evaluateResponse = await fetch('http://127.0.0.1:8000/evaluate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ answers })
});

const result = await evaluateResponse.json();
console.log(result.scores);
console.log(result.diagnosis);
console.log(result.recommendations);
```

## 📝 다음 단계

* [ ] 사용자 인증 시스템
* [ ] 평가 이력 저장 (DB)
* [ ] 다양한 난이도의 지문 추가
* [ ] 프론트엔드 UI 개발
* [ ] 학습 진도 추적 기능
