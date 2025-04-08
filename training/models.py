from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Custom User model for Employee, Trainer, Admin roles
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('trainer', 'Trainer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    enrolled_courses = models.ManyToManyField(
        'Course',
        blank=True,
        related_name='enrolled_by_users'  # Unique related_name for reverse query
    )

    def __str__(self):
        return self.username


# Course Model
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    trainer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='created_courses'  # Unique related_name for trainers
    )
    enrolled_employees = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name='enrolled_in_courses'  # Unique related_name for reverse query
    )
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    pre_test = models.ForeignKey('Quiz', on_delete=models.SET_NULL, related_name='pre_test_courses', blank=True, null=True)
    post_test = models.ForeignKey('Quiz', on_delete=models.SET_NULL, related_name='post_test_courses', blank=True, null=True)
    materials = models.TextField()

    def __str__(self):
        return self.title


# Quiz Model
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Question Model
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()  # The question text
    choice_1 = models.CharField(max_length=255)  # First option
    choice_2 = models.CharField(max_length=255)  # Second option
    choice_3 = models.CharField(max_length=255)  # Third option
    choice_4 = models.CharField(max_length=255)  # Fourth option
    correct_option = models.IntegerField(default=1)  # Correct option (1, 2, 3, or 4)

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
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='training_modules', blank=True, null=True)
    custom_course_id = models.CharField(max_length=50, unique=True, help_text="Unique identifier for the course")
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()  # HTML or rich text for module content
    duration = models.PositiveIntegerField(default=30, help_text="Duration in minutes")
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the module is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update when the module is modified
    is_active = models.BooleanField(default=True)  # To mark if the module is active or archived
    thumbnail = models.ImageField(upload_to='module_thumbnails/', blank=True, null=True)  # Optional thumbnail for the module

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
    started_at = models.DateTimeField(auto_now_add=True)  # Automatically set when progress starts
    time_spent = models.PositiveIntegerField(blank=True, null=True, help_text="Time spent in minutes")  # Track engagement time
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update when progress is modified
    completed_at = models.DateTimeField(blank=True, null=True)  # Track when the module is completed
    feedback = models.TextField(blank=True, null=True)  # Trainer comments or feedback

    def __str__(self):
        return f'{self.user.username} - {self.module.course.title} - {self.status}'

