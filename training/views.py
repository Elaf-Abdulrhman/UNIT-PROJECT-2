from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .forms import (
    UserRegistrationForm,
    CourseForm,
    QuizForm,
    AssignmentForm,
    QuestionForm,
    CustomUserCreationForm,
)
from .models import (
    Quiz,
    QuizResult,
    Progress,
    Course,
    Assignment,
    Question,
)

# views.py
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'training/signup_signin/signup.html', {'form': form})


# User Profile
@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserRegistrationForm(instance=user)
    return render(request, 'training/profile.html', {'form': form})


# Homepage
def home(request):
    courses = Course.objects.all()  # Retrieve all courses
    return render(request, 'training/home.html', {'courses': courses})


# Dashboard
@login_required
def dashboard(request):
    user = request.user
    progress = Progress.objects.filter(user=user)
    return render(request, 'training/dashboard.html', {'progress': progress})


# Complete Quiz
@login_required
def complete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            score = form.calculate_score()  # Add custom logic to calculate the score
            QuizResult.objects.create(user=request.user, quiz=quiz, score=score)
            return redirect('dashboard')
    else:
        form = QuizForm(quiz=quiz)
    return render(request, 'training/complete_quiz.html', {'quiz': quiz, 'form': form})


# Logout
def custom_logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out!')
    return redirect('home')


# About Page
def about(request):
    return render(request, 'training/about.html')


# Course Management
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'training/courses/course_list.html', {'courses': courses})


@login_required
def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.trainer = request.user
            course.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'training/courses/course_add.html', {'form': form})


@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk, trainer=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form})


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk, trainer=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


@login_required
def enrolled_employees(request, course_id):
    course = get_object_or_404(Course, id=course_id, trainer=request.user)
    employees = course.enrolled_employees.all()
    return render(request, 'data_analysis/enrolled_employees.html', {'course': course, 'employees': employees})


@login_required
def track_progress(request, course_id):
    course = get_object_or_404(Course, id=course_id, trainer=request.user)
    employees = course.enrolled_employees.all()
    progress_data = [
        {
            'employee': employee,
            'progress': '50%',  # Replace with actual progress calculation
            'performance': 'Good',  # Replace with actual performance data
        }
        for employee in employees
    ]
    return render(request, 'data_analysis/track_progress.html', {'course': course, 'progress_data': progress_data})


# Enroll in Course
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.role == 'employee':
        course.enrolled_employees.add(request.user)
        return redirect('course_list')
    else:
        return HttpResponseForbidden("You are not allowed to enroll in this course.")


# Quiz Management
@login_required
def create_quiz(request, course_id):
    course = get_object_or_404(Course, id=course_id, trainer=request.user)
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = QuizForm()
    return render(request, 'training/create_quiz.html', {'form': form, 'course': course})


# Assignment Management
@login_required
def create_assignment(request, course_id):
    course = get_object_or_404(Course, id=course_id, trainer=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = AssignmentForm()
    return render(request, 'training/create_assignment.html', {'form': form, 'course': course})


# Add Question to Quiz
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('quiz_detail', quiz_id=quiz.id)
    else:
        form = QuestionForm()
    return render(request, 'training/add_question.html', {'form': form, 'quiz': quiz})


# Course Detail
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'training/course_detail.html', {'course': course})


# Quiz Detail
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'training/quiz_detail.html', {'quiz': quiz})


def services(request):
    return render(request, 'training/services.html')


from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'training/signup_signin/login.html'  # Path to your login.html