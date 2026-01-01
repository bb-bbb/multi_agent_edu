# agents/recommendation_agent.py

class RecommendationAgent:
    """
    진단 결과를 기반으로 맞춤 학습 방법 추천
    """
    
    def __init__(self):
        self.recommendations = {
            "beginner": {
                "reading_comprehension": [
                    "짧은 영어 동화책이나 graded readers로 시작하세요",
                    "문장 단위로 천천히 읽으며 의미 파악하기",
                    "매일 10분씩 쉬운 영어 기사 읽기 (예: News in Levels)"
                ],
                "grammar": [
                    "기초 문법책으로 기본 시제부터 학습하세요",
                    "문법 앱(듀오링고, 퀴즐렛)으로 매일 연습하기",
                    "간단한 문장 만들기 연습"
                ],
                "vocabulary": [
                    "일상 생활 필수 단어 500개부터 암기하세요",
                    "단어장 앱 활용 (Anki, Quizlet)",
                    "영어 단어를 이미지와 연결하여 학습하기"
                ],
                "general": [
                    "기초부터 차근차근 학습하는 것이 중요합니다",
                    "하루 30분씩 꾸준히 학습하세요",
                    "초급 영어 유튜브 채널 구독 추천"
                ]
            },
            "intermediate": {
                "reading_comprehension": [
                    "중급 영어 소설이나 뉴스 기사를 읽으세요",
                    "읽은 내용을 요약하는 연습하기",
                    "영어 팟캐스트나 TED 강연 시청"
                ],
                "grammar": [
                    "복잡한 문장 구조 학습 (관계대명사, 접속사)",
                    "영작 연습으로 문법 적용력 키우기",
                    "온라인 문법 퀴즈 풀기"
                ],
                "vocabulary": [
                    "주제별 어휘 확장 (비즈니스, 학술 등)",
                    "동의어, 반의어 학습으로 어휘력 확장",
                    "영영 사전 활용하기"
                ],
                "general": [
                    "실전 영어 사용 기회를 늘리세요",
                    "영어 일기 쓰기 도전",
                    "온라인 언어 교환 파트너 찾기"
                ]
            },
            "advanced": {
                "reading_comprehension": [
                    "전문 서적이나 학술 논문 읽기",
                    "영어 원서 독서 모임 참여",
                    "복잡한 주제의 영어 컨텐츠 소비"
                ],
                "grammar": [
                    "고급 문법 표현 학습 (도치, 생략 등)",
                    "원어민 수준의 글쓰기 연습",
                    "문법 오류 교정 연습"
                ],
                "vocabulary": [
                    "전문 분야 어휘 학습",
                    "숙어와 관용 표현 마스터",
                    "문맥에 따른 뉘앙스 차이 학습"
                ],
                "general": [
                    "원어민 수준 유지를 위한 꾸준한 노출",
                    "영어로 생각하고 표현하는 연습",
                    "고급 영어 자격증 도전 (TOEFL, IELTS)"
                ]
            }
        }

    def recommend(self, diagnosis: dict) -> dict:
        """
        진단 결과 기반 학습 방법 추천
        
        Args:
            diagnosis: {
                "level": "intermediate",
                "weakness": ["어휘"],
                "diagnosis_summary": "..."
            }
            
        Returns:
            {
                "level_advice": "...",
                "weakness_recommendations": [...],
                "general_tips": [...]
            }
        """
        level = diagnosis.get("level", "beginner")
        weaknesses = diagnosis.get("weakness", [])
        
        # 수준별 기본 조언
        level_map = {
            "beginner": "초급",
            "intermediate": "중급",
            "advanced": "고급"
        }
        
        level_advice = f"{level_map.get(level, '초급')} 학습자를 위한 추천입니다."
        
        # 약점 영역별 추천
        weakness_recommendations = []
        area_map = {
            "독해": "reading_comprehension",
            "문법": "grammar",
            "어휘": "vocabulary"
        }
        
        for weakness in weaknesses:
            area_key = area_map.get(weakness)
            if area_key and area_key in self.recommendations.get(level, {}):
                weakness_recommendations.extend(
                    self.recommendations[level][area_key]
                )
        
        # 일반 학습 팁
        general_tips = self.recommendations.get(level, {}).get("general", [])
        
        return {
            "level_advice": level_advice,
            "weakness_recommendations": weakness_recommendations if weakness_recommendations else ["모든 영역이 우수합니다! 현재 수준을 유지하세요."],
            "general_tips": general_tips
        }

