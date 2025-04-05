from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

# Custom User model for Employee, Trainer, Admin roles
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('trainer', 'Trainer'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

    def __str__(self):
        return self.username

# Training Module Model
class TrainingModule(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField()  # Link to training video
    vr_video_url = models.URLField(blank=True, null=True)  # Link to VR/360° video (optional)
    trainer = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, related_name='training_modules')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Quiz Model (Multiple Questions per Quiz)
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    training_module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE, related_name='quizzes')
    
    def __str__(self):
        return self.title

# Question Model (For Storing Quiz Questions)
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    choice_1 = models.CharField(max_length=255)
    choice_2 = models.CharField(max_length=255)
    choice_3 = models.CharField(max_length=255)
    choice_4 = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

# QuizResult Model (To Store User Results After Completing a Quiz)
class QuizResult(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()  # Store the user's score (out of 100 or max possible score)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.quiz.title} - {self.score}'

# Progress Model (To Track Employee Progress on Training Modules)
class Progress(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='progress')
    training_module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE, related_name='progress')
    status = models.CharField(max_length=20, choices=[('in_progress', 'In Progress'), ('completed', 'Completed')], default='in_progress')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.training_module.title} - {self.status}'

# TrainingVideo Model
class TrainingVideo(models.Model):
    title = models.CharField(max_length=200)
    video_url = models.URLField()  # URL for the video (can be hosted on a video platform)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    video_type = models.CharField(max_length=50, choices=[('360', '360-degree'), ('VR', 'VR')])

# Test Model
class Test(models.Model):
    video = models.ForeignKey(TrainingVideo, related_name='tests', on_delete=models.CASCADE)
    question = models.TextField()
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)
    correct_answer = models.IntegerField()

# UserProgress Model
class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(TrainingVideo, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    test_score = models.IntegerField(null=True, blank=True)
    date_started = models.DateTimeField(auto_now_add=True)

# Course Model
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    trainer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses')
    start_date = models.DateField()
    end_date = models.DateField()
    materials = models.FileField(upload_to='course_materials/', blank=True, null=True)

    def __str__(self):
        return self.title

