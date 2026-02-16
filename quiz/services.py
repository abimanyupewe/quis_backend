
import os
import json
import google.generativeai as genai
from .models import QuizSession, Question, Option

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

def generate_questions_data(topic: str, num_questions: int = 5):
    """
    Fetches actual quiz data from Gemini for a given topic.
    Returns a list of question dictionaries.
    """
    if not GOOGLE_API_KEY:
        raise Exception("GOOGLE_API_KEY is not set")

    # Use gemini-flash-latest (Maps to stable Flash model with standard free tier)
    model = genai.GenerativeModel("gemini-flash-latest")
    
    prompt = f"""
    Buat {num_questions} soal kuis pilihan ganda bahasa Indonesia tentang topik: "{topic}".
    
    Instruksi Khusus:
    1. Jika topik berkaitan dengan Coding/Programming (Python, JS, dll), sertakan potongan code snippet yang relevan dalam teks pertanyaan jika perlu.
    2. Setiap soal wajib memiliki 4 pilihan jawaban dan hanya 1 yang benar.
    3. Output WAJIB JSON array murni tanpa markdown formatting (```json ... ```).
    
    Struktur JSON:
    [
        {{
            "text": "Pertanyaan (bisa multiline)",
            "options": [
                {{"text": "Pilihan A", "is_correct": false}},
                {{"text": "Pilihan B", "is_correct": true}},
                ...
            ]
        }}
    ]
    """
    
    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        quiz_text = response.text.strip()
        
        if quiz_text.startswith("```json"):
            quiz_text = quiz_text[7:]
        if quiz_text.endswith("```"):
            quiz_text = quiz_text[:-3]
            
        return json.loads(quiz_text)
    except Exception as e:
        raise Exception(f"Failed to generate quiz from Gemini: {str(e)}")

def save_questions_to_session(session: QuizSession, quiz_data: list):
    """
    Saves parsed quiz data to the database linked to the given session.
    """
    for q_data in quiz_data:
        question = Question.objects.create(session=session, text=q_data['text'])
        for opt_data in q_data['options']:
            Option.objects.create(
                question=question,
                text=opt_data['text'],
                is_correct=opt_data['is_correct']
            )

def generate_quiz_from_gemini(topic: str, num_questions: int = 5) -> QuizSession:
    """
    Creates a NEW session and populates it.
    """
    quiz_data = generate_questions_data(topic, num_questions)
    session = QuizSession.objects.create(topic=topic)
    save_questions_to_session(session, quiz_data)
    return session
