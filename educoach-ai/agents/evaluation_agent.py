import anthropic
import os
import json

class EvaluationAgent:
    """
    고정 지문 기반 독해 평가 에이전트
    - 독해 (Reading Comprehension): 지문 이해도
    - 문법 (Grammar): 답변의 문법 정확도
    - 어휘 (Vocabulary): 답변의 어휘 수준
    """
    
# 고정 지문
    PASSAGE = """Many people believe that success is only about talent or luck, but in reality, persistence plays a much bigger role. History shows countless examples of individuals who failed many times before achieving their goals. For instance, Thomas Edison tested thousands of materials before inventing the light bulb. His determination proved that consistent effort can lead to remarkable results.
In modern society, persistence is still essential. Students who continue studying even after facing difficulties often perform better than those who give up quickly. Similarly, athletes train for years to improve their skills, even when progress seems slow. These examples remind us that success is not a single event but a journey that requires patience and hard work."""
    
# 평가질문들
    QUESTIONS = [
        "What is the main idea of this passage?",
        "Give an example from the passage that supports the importance of persistence.",
        "In your own words, explain why persistence is important in modern society."
    ]
    
    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        print("ANTHROPIC_API_KEY loaded:", bool(api_key))
        self.client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
    
    # 3️⃣ 지문 + 질문 제공 (GET /passage)
    def get_passage(self):
        return {
            "passage": self.PASSAGE,
            "questions": self.QUESTIONS
        }
    

    def evaluate(self, answers: list[str]) -> dict:
        """
        사용자 답변을 평가하여 3개 영역의 점수 반환
        
        Args:
            answers: ["답변1", "답변2", "답변3"] (질문 순서대로)
            
        Returns:
            {
                "reading_comprehension": 75,
                "grammar": 65,
                "vocabulary": 80,
                "feedback": "..."
            }
        """
        
        # 답변들을 하나의 텍스트로 합치기
        answers_text = "\n".join([f"Q{i+1}: {ans}" for i, ans in enumerate(answers)])
        
        prompt = f"""다음은 영어 독해 지문과 학생의 답변입니다.
<passage>
{self.PASSAGE}
</passage>

<questions>
{chr(10).join([f"{i+1}. {q}" for i, q in enumerate(self.QUESTIONS)])}
</questions>

<student_answers>
{answers_text}
</student_answers>

다음 3가지 영역을 0-100점 척도로 평가하고, JSON 형식으로만 답변해주세요:

1. **reading_comprehension (독해력)**: 
   - 지문의 주제를 정확히 파악했는가?
   - 세부 내용을 이해하고 있는가?
   - 예시를 적절히 활용했는가?

2. **grammar (문법)**: 
   - 문장 구조가 올바른가?
   - 시제 사용이 정확한가?
   - 품사 사용이 적절한가?

3. **vocabulary (어휘)**: 
   - 적절한 단어를 선택했는가?
   - 어휘의 다양성이 있는가?
   - 고급 어휘를 사용했는가?

**반드시 아래 JSON 형식으로만 응답하세요:**

{{
  "reading_comprehension": 점수(0-100),
  "grammar": 점수(0-100),
  "vocabulary": 점수(0-100),
  "feedback": "전반적인 평가 코멘트 (2-3문장)"
}}"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = message.content[0].text.strip()
            
            # JSON 마크다운 제거
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            scores = json.loads(response_text)
            
            return {
                "reading_comprehension": int(scores.get("reading_comprehension", 50)),
                "grammar": int(scores.get("grammar", 50)),
                "vocabulary": int(scores.get("vocabulary", 50)),
                "feedback": scores.get("feedback", "평가가 완료되었습니다.")
            }
            
        except Exception as e:
            print(f"Error in evaluation: {e}")
            print(f"Response text: {response_text if 'response_text' in locals() else 'N/A'}")
            return {
                "reading_comprehension": 50,
                "grammar": 50,
                "vocabulary": 50,
                "feedback": "평가 중 오류가 발생했습니다."
            }