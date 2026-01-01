# 🎯 평가 항목 (3개만)

# Vocabulary (어휘) / Grammar (문법) / Reading Comprehension (독해)


# 학습 진단 기준 정의 (핵심)

# | 점수     | 수준           |
# | ------ | ------------ |
# | 0–59   | Beginner     |
# | 60–79  | Intermediate |
# | 80–100 | Advanced     |


# # 출력 포맷(고정)

# {
#   "level": "intermediate",
#   "weakness": ["reading"],
#   "diagnosis_summary": "독해 영역에서 낮은 성취도를 보입니다."
# } 

# -> 구조는 나중에 컨텍스트 엔지니어링의 핵심 데이터가 됨


# agents/diagnosis_agent.py

class DiagnosisAgent:
    def __init__(self):
        self.level_thresholds = {
            "beginner": 59,
            "intermediate": 79
        }

    def determine_level(self, scores: dict) -> str:
        score_values = []

        for v in scores.values():
            # case 1: dict 안에 score가 있는 경우
            if isinstance(v, dict) and "score" in v:
                score_values.append(v["score"])

            # case 2: 그냥 숫자인 경우
            elif isinstance(v, (int, float)):
                score_values.append(v)

        # 방어 코드 (아예 점수가 없을 때)
        if not score_values:
            return "unknown"

        average_score = sum(score_values) / len(score_values)

        if average_score >= 80:
            return "advanced"
        elif average_score >= 60:
            return "intermediate"
        else:
            return "beginner"

    def detect_weakness(self, scores: dict) -> list:
        weakest_area = min(scores, key=scores.get)
        weaknesses = []

        if scores[weakest_area] < 60:
            weaknesses.append(weakest_area)

        return weaknesses

    def diagnose(self, scores: dict) -> dict:
        level = self.determine_level(scores)
        weaknesses = self.detect_weakness(scores)

        summary = (
            f"{', '.join(weaknesses)} 영역에서 상대적으로 낮은 성취도를 보입니다."
            if weaknesses
            else "전반적으로 안정적인 독해 실력을 보입니다."
        )

        return {
            "level": level,
            "weakness": weaknesses,
            "diagnosis_summary": summary
        }

