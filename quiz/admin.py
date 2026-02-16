
from django.contrib import admin
from django.contrib import messages
from .models import QuizSession, Question, Option
from .services import generate_questions_data, save_questions_to_session

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ('text', 'session')

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'target_question_count', 'id', 'created_at', 'question_count')
    readonly_fields = ('id', 'created_at')
    actions = ['generate_questions']

    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'

    @admin.action(description='Generate Questions from Gemini')
    def generate_questions(self, request, queryset):
        success_count = 0
        for session in queryset:
            try:
                # Generate new questions
                quiz_data = generate_questions_data(session.topic, session.target_question_count)
                # Save to session
                save_questions_to_session(session, quiz_data)
                success_count += 1
            except Exception as e:
                self.message_user(request, f"Error generating for '{session.topic}': {e}", level=messages.ERROR)
        
        self.message_user(request, f"Successfully generating questions for {success_count} sessions.", level=messages.SUCCESS)

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct',)
