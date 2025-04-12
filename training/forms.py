# forms.py (in your app)

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Course, Blog, Video
from django.forms import modelformset_factory, inlineformset_factory



# User Registration Form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser  # Use the custom user model
        fields = ['username', 'email', 'password1', 'password2', 'role', 'first_name', 'last_name'] 


# Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True, label="Role")
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role', 'first_name', 'last_name')

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


class CourseForm(forms.ModelForm):
    
    # Custom date input format for start_date and end_date
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Start Date"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="End Date"
    )
    video_url = forms.URLField(
        required=False,
        label="Video URL",
        help_text="Optional: Add a video URL for this course."
    )

    class Meta:
        model = Course
        fields = ['title', 'description', 'image', 'start_date', 'end_date', 'video_url']


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_url']


