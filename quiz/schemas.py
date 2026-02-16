
from ninja import Schema
from uuid import UUID
from typing import List

class GenerateQuizRequest(Schema):
    topic: str
    num_questions: int = 5

class OptionOutSchema(Schema):
    id: UUID
    text: str
    # IMPORTANT: is_correct is excluded to prevent leaking answers

class OptionWithAnswerSchema(Schema):
    id: UUID
    text: str
    is_correct: bool

class QuestionOutSchema(Schema):
    id: UUID
    text: str
    options: List[OptionOutSchema]

class QuestionWithAnswerSchema(Schema):
    id: UUID
    text: str
    options: List[OptionWithAnswerSchema]

class QuizSessionResponse(Schema):
    id: UUID
    topic: str
    questions: List[QuestionOutSchema]

class QuizSessionReviewResponse(Schema):
    id: UUID
    topic: str
    questions: List[QuestionWithAnswerSchema]

class AnswerSchema(Schema):
    question_id: UUID
    selected_option_id: UUID

class SubmitAnswersRequest(Schema):
    answers: List[AnswerSchema]

class SubmitAnswersResponse(Schema):
    final_score: float
    total_correct: int
    total_wrong: int

class UserSchema(Schema):
    username: str
    email: str = None

class RegisterRequest(Schema):
    username: str
    password: str
    email: str = None
