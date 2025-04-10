from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .forms import QuestionFormSet
from .forms import (
    CourseForm,
    QuizForm,
    CustomUserCreationForm,
)
from .models import (
    Progress,
    Course,
    Course, 
    Quiz, 
    UserQuizAttempt,
    Enrollment,  
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
    return render(request, 'signup_signin/signup.html', {'form': form})


# User Profile
@login_required
def profile(request):
    if request.user.is_authenticated:
        if request.user.role == 'employee':
            # Fetch enrolled courses for employees
            enrollments = Enrollment.objects.filter(user=request.user)
            return render(request, 'training/profile.html', {'enrollments': enrollments})
        elif request.user.role == 'trainer':
            # Fetch created courses for trainers
            created_courses = Course.objects.filter(trainer=request.user)
            return render(request, 'training/profile.html', {'created_courses': created_courses})
    return redirect('login')


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
    search_query = request.GET.get('search', '')  # Get the search query
    sort_by = request.GET.get('sort', '')  # Get the sorting option, default to no sorting

    # Filter courses based on the search query
    if search_query:
        courses = Course.objects.filter(title__icontains=search_query)
    else:
        courses = Course.objects.all()

    # Apply sorting if a valid option is selected
    if sort_by == 'start_date':
        courses = courses.order_by('start_date')  # Earliest starting date first

    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'search_query': search_query,
        'sort_by': sort_by,
    })


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

    return render(request, 'courses/course_edit.html', {'form': form, 'course': course})


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

    return render(request, 'courses/course_add.html', {'form': form})


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)  # Fetch the course or return a 404 error
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')  # Redirect to the course list after deletion
    return render(request, 'courses/course_delete.html', {'course': course})


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

    # Ensure only the trainer of the course can add quizes
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

    return render(request, 'training/quizes/create_quiz.html', {'form': form, 'course': course, 'quiz_type': quiz_type})


# Course Detail
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})


def services(request):
    return render(request, 'training/services.html')

class CustomLoginView(LoginView):
    template_name = 'signup_signin/login.html'  # Path to your login.html


@login_required
def start_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.is_authenticated and request.user.role == 'employee':
        # Check if the user is already enrolled
        enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
        if created:
            # Enrollment was successfully created
            return redirect('profile')
        else:
            # User is already enrolled
            return redirect('profile')
    return redirect('course_list')


def show_quiz(request, course_id, quiz_type):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user is enrolled
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        return redirect('course_detail', course_id=course.id)

    # Get the quiz (pre or post)
    is_pre = True if quiz_type == "pre" else False
    quiz = Quiz.objects.filter(course=course, is_pre_course=is_pre).first()

    if not quiz:
        return render(request, 'quiz/not_found.html')

    # Check if user already completed it
    if UserQuizAttempt.objects.filter(user=request.user, quiz=quiz).exists():
        return render(request, 'quiz/already_done.html')

    return render(request, 'quiz/take_quiz.html', {'quiz': quiz})


@login_required
#@user_passes_test(lambda u: u.is_staff)
def create_quiz(request):
    courses = Course.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        course_id = request.POST.get('course_id')
        is_pre = request.POST.get('is_pre_course') == 'on'

        course = Course.objects.get(id=course_id)
        quiz = Quiz.objects.create(title=title, course=course, is_pre_course=is_pre)
        return redirect('add_questions', quiz_id=quiz.id)

    return render(request, 'create_quiz.html', {'courses': courses})

def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        formset = QuestionFormSet(request.POST, queryset=Question.objects.none())

        if formset.is_valid():
            for form in formset:
                question = form.save(commit=False)
                question.quiz = quiz
                question.save()
            return redirect('dashboard')  # or redirect to 'add_choices' per question
    else:
        formset = QuestionFormSet(queryset=Question.objects.none())

    return render(request, 'add_questions.html', {
        'quiz': quiz,
        'formset': formset
    })
