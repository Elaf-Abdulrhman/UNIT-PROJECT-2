from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .forms import (
    CourseForm,
    CustomUserCreationForm,
)
from .models import (
    Course, 
    Enrollment,  
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
    return render(request, 'training/dashboard.html')


# About Page
def about(request):
    return render(request, 'training/about.html')

def course_list(request):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '')

    if search_query:
        courses = Course.objects.filter(
            Q(title__icontains=search_query) |
            Q(trainer__first_name__icontains=search_query) |
            Q(trainer__last_name__icontains=search_query)
        )
    else:
        courses = Course.objects.all()

    if sort_by == 'start_date':
        courses = courses.order_by('start_date')

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

# Enroll in Course
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.role == 'employee':
        course.enrolled_employees.add(request.user)
        return redirect('course_list')
    else:
        return HttpResponseForbidden("You are not allowed to enroll in this course.")


# Course Detail
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})


def services(request):
    return render(request, 'training/services.html')

class CustomLoginView(LoginView):
    template_name = 'signup_signin/login.html'  # Path to your login.html

