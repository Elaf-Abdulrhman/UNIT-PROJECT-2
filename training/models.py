from django.db import models
from django.contrib.auth.models import AbstractUser
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


# Course Model
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    materials = models.FileField(upload_to='course_materials/', blank=True, null=True)
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    enrolled_employees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='enrolled_courses', blank=True)

    def __str__(self):
        return self.title


# Quiz Model
class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Question Model
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()  # The question text
    option_1 = models.CharField(max_length=255)  # First option
    option_2 = models.CharField(max_length=255)  # Second option
    option_3 = models.CharField(max_length=255)  # Third option
    option_4 = models.CharField(max_length=255)  # Fourth option
    correct_option = models.IntegerField()  # Correct option (1, 2, 3, or 4)

    def __str__(self):
        return self.text


# QuizResult Model
class QuizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField()  # Store the user's score (out of 100 or max possible score)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.quiz.title} - {self.score}'


# Assignment Model
class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    file_upload = models.FileField(upload_to='assignments/', blank=True, null=True)

    def __str__(self):
        return self.title


# Interactive Module Model
class InteractiveModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='interactive_modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    content = models.TextField()  # HTML or rich text for interactive content

    def __str__(self):
        return self.title


# Training Module Model
class TrainingModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='training_modules')
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()  # HTML or rich text for module content

    def __str__(self):
        return self.title


# Progress Model (To Track Employee Progress on Training Modules)
class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress')
    status = models.CharField(max_length=20, choices=[('in_progress', 'In Progress'), ('completed', 'Completed')], default='in_progress')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.title} - {self.status}'

