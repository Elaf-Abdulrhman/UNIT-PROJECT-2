from django.contrib import admin
from .models import TrainingModule, Quiz, QuizResult, Progress, CustomUser  # Import all models

# Register all models
admin.site.register(TrainingModule)
admin.site.register(Quiz)
admin.site.register(QuizResult)
admin.site.register(Progress)
admin.site.register(CustomUser)
