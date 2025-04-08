# forms.py (in your app)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Course, Quiz, Assignment, TrainingModule, Question, InteractiveModule


# User Registration Form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser  # Use the custom user model
        fields = ['username', 'email', 'password1', 'password2', 'role']  # Include role if using CustomUser


# Quiz Form
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']


# Assignment Form
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'file_upload']  # Include file_upload
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


# Training Module Form
class TrainingModuleForm(forms.ModelForm):
    class Meta:
        model = TrainingModule
        fields = ['title', 'description', 'content']


# Course Form
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'image', 'start_date', 'end_date', 'trainer']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


# Question Form
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'choice_1', 'choice_2', 'choice_3', 'choice_4', 'correct_option']


# Interactive Module Form
class InteractiveModuleForm(forms.ModelForm):
    class Meta:
        model = InteractiveModule
        fields = ['title', 'description', 'content']

