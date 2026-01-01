
---

```markdown
# EduCoach AI  
**개인화 학습을 위한 교육 특화 Multi-Agent AI 시스템**

EduCoach AI는 대형 언어 모델(LLM)과 **멀티 에이전트 아키텍처**를 활용하여  
학습 진단, 학습 추천, 실시간 코칭을 지원하는 **교육 특화 AI 시스템**입니다.

이 프로젝트는 교육 도메인에서  
**AI Agent 설계, 컨텍스트 엔지니어링, RAG 파이프라인**을  
어떻게 구조적으로 적용할 수 있는지를 탐구하는 것을 목표로 합니다.

---

## Overview

최근 LLM은 강력한 성능을 보여주고 있지만,  
학습자의 수준, 목표, 학습 이력과 같은 **개인 맥락을 구조적으로 이해하는 데에는 한계**가 있습니다.

EduCoach AI는 이러한 문제를 해결하기 위해 다음과 같은 접근을 사용합니다.

- 역할이 분리된 AI Agent 설계
- 학습자 중심 컨텍스트 구조화
- 검색 기반(RAG) 동적 정보 주입

본 프로젝트는 상용 서비스를 목표로 하기보다는,  
**교육 AI Agent 시스템의 설계 사고와 구현 패턴을 공유**하는 데 초점을 둡니다.

---

## Key Features

- 학습 진단·추천·코칭을 위한 Multi-Agent 구조
- 학습자 프로파일 기반 동적 컨텍스트 구성
- 교육 자료를 활용한 RAG 파이프라인
- OpenAI / Anthropic 등 LLM 벤더 독립적 설계
- RESTful Backend API 및 프로토타입 Frontend 제공

---

## System Architecture

본 시스템은 오케스트레이터를 중심으로 여러 전문 Agent가 협력하는 구조로 설계되었습니다.

```

User
↓
Orchestrator Agent
↓
┌──────────────────┬────────────────────┬──────────────────┐
| Diagnosis Agent | Recommendation Agent | Coaching Agent |
└──────────────────┴────────────────────┴──────────────────┘
↓
RAG / Context Layer
↓
LLM

```

각 Agent는 명확한 역할과 책임을 가지며,  
단일 프롬프트 기반 시스템보다 **확장성과 유지보수성이 뛰어난 구조**를 제공합니다.

---

## Agents Design

### Diagnosis Agent
- 학습자 프로파일 및 학습 이력 분석
- 취약 영역 및 학습 수준 진단

### Recommendation Agent
- 다음 학습 주제 및 자료 추천
- 검색된 교육 콘텐츠 기반 추천 수행

### Coaching Agent
- 실시간 학습 피드백 제공
- 학습자 수준에 맞춘 설명 깊이 조절

### Orchestrator
- Agent 실행 순서 관리
- Agent 결과를 종합하여 최종 응답 생성

---

## Context Engineering

본 프로젝트에서는 **컨텍스트를 단순한 텍스트가 아닌 설계 요소**로 취급합니다.

### 컨텍스트 구성 요소
- 학습자 프로파일 (수준, 목표, 약점)
- 학습 이력 (학습 주제, 점수, 진행 상황)
- RAG를 통해 검색된 교육 자료
- 현재 수행 중인 학습 태스크 상태

요청마다 고정된 프롬프트를 사용하는 대신,  
**상황에 따라 동적으로 컨텍스트를 조합**합니다.

예시 (단순화):

```json
{
  "learner_level": "중급",
  "goal": "TOEIC 900",
  "weakness": ["독해 Part 7"],
  "current_task": "학습 진단"
}
```

---

## RAG Pipeline

1. 교육 자료(PDF, 노트 등) 수집
2. 문서 분할(Chunking) 및 임베딩 생성
3. 벡터 데이터베이스에 저장
4. 태스크에 따라 관련 문서 검색
5. 검색 결과를 Agent 컨텍스트에 주입

설계 시 고려 사항:

* Chunk 크기와 검색 정확도의 균형
* Top-k 조절을 통한 비용 및 응답 품질 최적화

---

## Prompt Design

* System / Task / Context 역할 분리
* Agent별 시스템 프롬프트 설계
* 프롬프트 버전 관리 및 실험 기록

본 프로젝트의 목표는
“한 번 잘 되는 프롬프트”가 아니라
**일관되고 재현 가능한 응답을 생성하는 구조**입니다.

---

## LLM Integration

LLM 벤더 종속성을 줄이기 위해 공통 인터페이스를 사용합니다.

지원 또는 확장 예정:

* OpenAI (GPT-4 / GPT-4o)
* Anthropic Claude (실험적)

설계 목표:

* 모델 교체 용이성
* 컨텍스트 길이 제어
* 비용 효율적인 호출

---

## API & Service Layer

Backend는 FastAPI 기반으로 구현되었으며,
RESTful 원칙에 따라 설계되었습니다.

주요 엔드포인트 예시:

* `POST /diagnose`
* `POST /recommend`
* `POST /coach`

API는 Frontend 및 외부 시스템 연동을 고려하여 설계되었습니다.

---

## Frontend (Prototype)

프로토타입 수준의 Frontend를 제공하여
Agent 동작 흐름과 사용자 경험을 검증합니다.

* UI 완성도보다 인터랙션 흐름에 집중
* 사용자 테스트 및 디버깅 목적

---

## Installation & Usage

```bash
git clone https://github.com/your-username/educoach-ai.git
cd educoach-ai

pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

필요 환경 변수:

* `OPENAI_API_KEY`
* `ANTHROPIC_API_KEY` (선택)

---

## Project Structure

```text
educoach-ai/
 ├── agents/
 ├── orchestration/
 ├── rag/
 ├── prompts/
 ├── api/
 ├── frontend/
 └── README.md
```

---

## Limitations

* 실제 교육 데이터가 아닌 단순화된 예제 데이터 사용
* 응답 품질에 대한 정량적 평가 지표 부족
* 세션 간 장기 메모리 미구현

---

## Future Work

* 음성·이미지 입력을 포함한 멀티모달 확장
* Agent 응답 품질 평가 체계 강화
* 실제 교육 데이터셋 연동
* 정교한 학습자 모델링

---

## Tech Stack

* Python
* LangChain / LangGraph
* FastAPI
* Vector Database (FAISS / Chroma)
* OpenAI / Anthropic API

---

## License

MIT License

---

## Acknowledgements

본 프로젝트는 다음 분야의 연구 및 오픈소스 프로젝트에서 영감을 받았습니다.

* LLM 기반 Agent 시스템
* Retrieval-Augmented Generation (RAG)
* 교육 분야 AI 응용
