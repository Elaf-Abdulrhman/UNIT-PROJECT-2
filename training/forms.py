# forms.py (in your app)

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Course, Quiz,TrainingModule, Question, InteractiveModule


# User Registration Form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser  # Use the custom user model
        fields = ['username', 'email', 'password1', 'password2', 'role']  # Include role if using CustomUser


# Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True, label="Role")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')  # Removed 'courses'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data.get('role')
        if commit:
            user.save()
        return user


# Custom User Change Form
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')  # Add any fields you want to include


# Quiz Form
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']


# Training Module Form
class TrainingModuleForm(forms.ModelForm):
    class Meta:
        model = TrainingModule
        fields = ['title', 'description', 'content']


# Course Form
class CourseForm(forms.ModelForm):
    pre_quiz = forms.ModelChoiceField(
        queryset=Quiz.objects.all(),
        required=False,
        label="Pre-Quiz"
    )
    post_quiz = forms.ModelChoiceField(
        queryset=Quiz.objects.all(),
        required=False,
        label="Post-Quiz"
    )

    class Meta:
        model = Course
        fields = ['title', 'description', 'image', 'start_date', 'end_date', 'pre_quiz', 'post_quiz']


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

