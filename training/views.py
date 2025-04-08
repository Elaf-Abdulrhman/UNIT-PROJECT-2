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
    if request.user.role == 'employee':
        # Fetch courses the employee is enrolled in
        enrolled_courses = request.user.enrolled_courses.all()  # Assuming a ManyToManyField for enrolled courses
        return render(request, 'training/profile.html', {'courses': enrolled_courses, 'role': 'employee'})
    elif request.user.role == 'trainer':
        # Fetch courses created by the trainer
        created_courses = Course.objects.filter(trainer=request.user)
        return render(request, 'training/profile.html', {'courses': created_courses, 'role': 'trainer'})
    else:
        # Handle other roles or unauthorized access
        return render(request, 'training/profile.html', {'courses': [], 'role': 'unknown'})


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


# About Page
def about(request):
    return render(request, 'training/about.html')


# Course Management
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'training/courses/course_list.html', {'courses': courses})


@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')  # Redirect to the course list after saving
    else:
        form = CourseForm(instance=course)

    return render(request, 'training/courses/course_edit.html', {'form': form, 'course': course})


@login_required
def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.trainer = request.user  # Automatically set the logged-in user as the trainer
            course.save()
            return redirect('course_list')  # Redirect to the course list after saving
    else:
        form = CourseForm()

    return render(request, 'training/courses/course_add.html', {'form': form})


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)  # Fetch the course or return a 404 error
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')  # Redirect to the course list after deletion
    return render(request, 'training/courses/course_delete.html', {'course': course})


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


@login_required
def create_quiz(request, course_id, quiz_type):
    course = get_object_or_404(Course, pk=course_id)

    # Ensure only the trainer of the course can add quizzes
    if request.user != course.trainer:
        return redirect('course_list')

    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()

            # Associate the quiz with the course
            if quiz_type == 'pre':
                course.pre_quiz = quiz
            elif quiz_type == 'post':
                course.post_quiz = quiz
            course.save()

            return redirect('course_detail', course_id=course.id)
    else:
        form = QuizForm()

    return render(request, 'quizes/create_quiz.html', {'form': form, 'course': course, 'quiz_type': quiz_type})


# Course Detail
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'training/courses/course_detail.html', {'course': course})


def services(request):
    return render(request, 'training/services.html')

class CustomLoginView(LoginView):
    template_name = 'training/signup_signin/login.html'  # Path to your login.html


@login_required
def start_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course = Course.objects.create(
        title="Sample Course",
        description="This is a sample course",
        trainer=request.user,
        image=None,
        # Remove 'start_date' and 'end_date' if they are being passed here
    )
    return render(request, 'training/courses/start_course.html', {'course': course})


@login_required
def solve_quiz(request, course_id, quiz_type):
    course = get_object_or_404(Course, pk=course_id)
    if quiz_type == 'pre':
        quiz = course.pre_quiz
    elif quiz_type == 'post':
        quiz = course.post_quiz
    else:
        return redirect('course_list')  # Redirect if quiz_type is invalid

    if request.method == 'POST':
        # Logic to handle quiz submission (e.g., calculate score, save progress)
        return redirect('course_list')  # Redirect after solving the quiz

    return render(request, 'training/quizzes/solve_quiz.html', {'quiz': quiz, 'quiz_type': quiz_type})


