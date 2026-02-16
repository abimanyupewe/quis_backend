
import os
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ninja import NinjaAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

from .models import QuizSession, Question, Option
from .schemas import (
    GenerateQuizRequest,
    QuizSessionResponse,
    SubmitAnswersRequest,
    SubmitAnswersResponse,
    RegisterRequest,
    UserSchema,
    QuizSessionReviewResponse
)
from .services import generate_quiz_from_gemini
from typing import List

# Use NinjaExtraAPI for JWT support
api = NinjaExtraAPI(
    title="Quiz Engine API",
    description="Dynamic Quiz API powered by Google Gemini 1.5 Pro",
    version="1.0.0"
)

# Register JWT Controller (Sign In, Refresh)
api.register_controllers(NinjaJWTDefaultController)

@api.post("/auth/signup", response=UserSchema)
def signup(request, payload: RegisterRequest):
    if User.objects.filter(username=payload.username).exists():
        raise Exception("Username already exists")
    
    user = User.objects.create(
        username=payload.username,
        email=payload.email,
        password=make_password(payload.password)
    )
    return user

@api.post("/quiz/generate/", response=QuizSessionResponse)
def generate_quiz(request, payload: GenerateQuizRequest):
    try:
        session = generate_quiz_from_gemini(payload.topic, payload.num_questions)
        return session
    except Exception as e:
        # Improve error handling in production
        raise Exception(f"Error generating quiz: {str(e)}")

@api.post("/quiz/{session_id}/submit/", response=SubmitAnswersResponse)
def submit_answers(request, session_id: str, payload: SubmitAnswersRequest):
    session = get_object_or_404(QuizSession, id=session_id)
    all_questions = session.questions.all()
    total_questions = all_questions.count()
    
    correct_count = 0
    
    for answer in payload.answers:
        try:
            option = Option.objects.get(id=answer.selected_option_id, question_id=answer.question_id)
            if option.question.session_id != session.id:
                continue
                
            if option.is_correct:
                correct_count += 1
        except Option.DoesNotExist:
            continue
            
    final_score = 0.0
    if total_questions > 0:
        final_score = (correct_count / total_questions) * 100
        
    return {
        "final_score": final_score,
        "total_correct": correct_count,
        "total_wrong": total_questions - correct_count
    }

@api.get("/quiz/history/", response=List[QuizSessionResponse])
def quiz_history(request):
    return QuizSession.objects.all().order_by('-created_at')

@api.get("/quiz/{session_id}/answers/", response=QuizSessionReviewResponse)
def get_quiz_with_answers(request, session_id: str):
    """
    Returns the quiz session WITH correct answers exposed.
    Intended for review after submission or for admin/teacher use.
    """
    session = get_object_or_404(QuizSession, id=session_id)
    return session
