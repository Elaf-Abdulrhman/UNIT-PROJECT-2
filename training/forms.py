# forms.py (in your app)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Import the custom user model if using one
from .models import Course

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser  # Use the custom user model
        fields = ['username', 'email', 'password1', 'password2', 'role']  # Include role if using CustomUser

class QuizForm(forms.Form):
    # Example fields
    question = forms.CharField(max_length=255)
    answer = forms.CharField(max_length=255)

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'start_date', 'end_date', 'materials']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

