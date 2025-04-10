from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings


# Custom User model for Employee, Trainer, Admin roles
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('trainer', 'Trainer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    enrolled_courses = models.ManyToManyField('Course', blank=True, related_name='enrolled_users')

    def __str__(self):
        return self.username


# Course Model
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_courses'
    )
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title


# Quiz Model
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_quizzes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Question Model
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()  # The question text

    def __str__(self):
        return self.text


# Choice Model (Dynamic Choices for Questions)
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)  # The choice text
    is_correct = models.BooleanField(default=False)  # Whether this choice is correct

    def __str__(self):
        return self.text


# Quiz Result Model (Consolidated)
class UserQuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    score = models.FloatField()  # Store the user's score
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.quiz.title} - {self.score}'


# Training Module Model
class TrainingModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='training_modules', blank=True, null=True)
    custom_course_id = models.CharField(max_length=50, unique=True, help_text="Unique identifier for the course")
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()  # HTML or rich text for module content
    duration = models.PositiveIntegerField(default=30, help_text="Duration in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    thumbnail = models.ImageField(upload_to='module_thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_duration_in_hours(self):
        """Convert duration from minutes to hours."""
        return f"{self.duration // 60}h {self.duration % 60}m" if self.duration else "N/A"


# Progress Model (To Track Employee Progress on Training Modules)
class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    course = models.ForeignKey(TrainingModule, on_delete=models.CASCADE, related_name='progress')
    completed = models.BooleanField(default=False)
    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    score = models.FloatField(blank=True, null=True)  # Optional score
    started_at = models.DateTimeField(auto_now_add=True)
    time_spent = models.PositiveIntegerField(blank=True, null=True, help_text="Time spent in minutes")
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.title} - {self.status}'


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} enrolled in {self.course.title}'
