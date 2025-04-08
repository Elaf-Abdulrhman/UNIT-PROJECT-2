from django.contrib import admin
from .models import Course, Quiz, TrainingModule, QuizResult, Progress, CustomUser  # Import all models

# Register all models
admin.site.register(TrainingModule)
admin.site.register(QuizResult)
admin.site.register(Progress)
admin.site.register(CustomUser)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'trainer', 'start_date', 'end_date')
    list_filter = ('trainer', 'start_date')
    search_fields = ('title', 'description')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
