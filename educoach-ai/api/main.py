# api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from agents.evaluation_agent import EvaluationAgent
from agents.diagnosis_agent import DiagnosisAgent
from agents.recommendation_agent import RecommendationAgent
import os

app = FastAPI(
    title="EduCoach AI",
    description="영어 독해 평가 및 학습 추천 시스템",
    version="1.0.0"
)

# CORS 설정 (프론트엔드 연동용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnswersRequest(BaseModel):
    """답변 제출 요청 모델"""
    answers: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "answers": [
                    "The main idea is that persistence is more important than talent for success.",
                    "Thomas Edison tested thousands of materials before inventing the light bulb.",
                    "Persistence helps students overcome difficulties and athletes improve their skills over time."
                ]
            }
        }


class EvaluationResponse(BaseModel):
    """평가 응답 모델"""
    scores: dict
    diagnosis: dict
    recommendations: dict


@app.get("/")
def root():
    """API 루트"""
    return {
        "message": "EduCoach AI API",
        "version": "1.0.0",
        "description": "영어 독해 평가 및 맞춤 학습 추천 시스템",
        "endpoints": {
            "지문 가져오기": "GET /passage",
            "답변 평가하기": "POST /evaluate"
        }
    }


@app.get("/passage")
def get_passage():
    """
    평가용 독해 지문과 질문 가져오기
    
    Returns:
        - passage: 독해 지문
        - questions: 평가 질문 리스트
    """
    evaluator = EvaluationAgent()
    return evaluator.get_passage()


@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate_answers(request: AnswersRequest):
    """
    답변 평가 → 진단 → 학습 추천
    
    1단계: 독해/문법/어휘 평가 (0-100점)
    2단계: 수준 진단 (Beginner/Intermediate/Advanced)
    3단계: 맞춤 학습 방법 추천
    
    Args:
        answers: 3개 질문에 대한 답변 리스트
    """
    
    # 답변 개수 확인
    if len(request.answers) != 3:
        raise HTTPException(
            status_code=400,
            detail="3개의 질문에 대한 답변이 필요합니다."
        )
    
    # 빈 답변 확인
    if any(not ans.strip() for ans in request.answers):
        raise HTTPException(
            status_code=400,
            detail="모든 질문에 답변해주세요."
        )
    
    try:
        # 1. 평가
        evaluator = EvaluationAgent()
        evaluation_result = evaluator.evaluate(request.answers)
        
        # feedback 제외하고 점수만 추출
        scores = {
            "reading_comprehension": evaluation_result["reading_comprehension"],
            "grammar": evaluation_result["grammar"],
            "vocabulary": evaluation_result["vocabulary"]
        }
        
        # 2. 진단
        diagnoser = DiagnosisAgent()
        diagnosis = diagnoser.diagnose(scores)
        
        # 3. 추천
        recommender = RecommendationAgent()
        recommendations = recommender.recommend(diagnosis)
        
        return {
            "scores": {
                **scores,
                "feedback": evaluation_result.get("feedback", "")
            },
            "diagnosis": diagnosis,
            "recommendations": recommendations
        }
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"평가 중 오류가 발생했습니다: {str(e)}"
        )


@app.get("/health")
def health_check():
    """헬스 체크"""
    return {"status": "healthy"}
