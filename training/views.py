from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, FileResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth.views import PasswordChangeView
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .forms import (
    CourseForm,
    CustomUserCreationForm,
    BlogForm,
    VideoForm,
)
from .models import (
    Course, 
    Enrollment,  
    Blog,
    Video,
    VideoProgress,
)
from .utils import generate_certificate

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
    search_query = request.GET.get('search', '')  # Get the search query
    sort_by = request.GET.get('sort', '')  # Get the sorting option, default to no sorting

    # Filter courses based on the search query (title or trainer name)
    if search_query:
        courses = Course.objects.filter(
            Q(title__icontains=search_query) | Q(trainer__username__icontains=search_query)
        )  # Search in course title or trainer username
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
    if request.user.role != 'trainer':  # Ensure only trainers can add courses
        return redirect('course_list')

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.trainer = request.user  # Assign the logged-in trainer as the course creator
            course.save()

            # Handle the optional video URL
            video_url = form.cleaned_data.get('video_url')
            if video_url:
                Video.objects.create(course=course, title=f"Intro Video for {course.title}", video_url=video_url)

            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form})


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


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    videos = course.videos.all()

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'videos': videos,
    })

def services(request):
    return render(request, 'training/services.html')

class CustomLoginView(LoginView):
    template_name = 'signup_signin/login.html'  # Path to your login.html

class PasswordResetView(View):
    def get(self, request):
        return render(request, 'signup_signin/reset/reset_password_form.html')

    def post(self, request):
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse('User does not exist', status=400)

        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(user.pk.encode('utf-8'))
        reset_url = reverse('password_reset_confirm', args=[uidb64, token])

        # Render a custom password reset page without email
        reset_page = render_to_string('signup_signin/reset/password_reset_confirmation.html', {'reset_url': reset_url})
        return HttpResponse(reset_page)

class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode('utf-8')
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            return HttpResponse('Invalid token', status=400)

        return render(request, 'signup_signin/reset/password_reset_confirm.html', {'uidb64': uidb64, 'token': token})

    def post(self, request, uidb64, token):
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = User.objects.get(pk=uid)

        # Handle password reset confirmation
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_reset_complete')
        else:
            return render(request, 'signup_signin/reset/password_reset_confirm.html', {'form': form})

def course_intro(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = False

    # Check if the user is enrolled
    if request.user.is_authenticated and request.user.role == 'employee':
        is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()

        # Handle enrollment if the user clicks "Enroll"
        if request.method == 'POST' and 'enroll' in request.POST:
            if not is_enrolled:  # Prevent duplicate enrollments
                Enrollment.objects.create(user=request.user, course=course)
                is_enrolled = True

    return render(request, 'courses/course_intro.html', {'course': course, 'is_enrolled': is_enrolled})

def blog_view(request):
    return render(request, 'blogs/blog.html')

def faq_view(request):
    return render(request, 'training/faq.html')

def blog_list(request):
    blogs = Blog.objects.all()  # Fetch all blog posts
    return render(request, 'blogs/blog.html', {'blogs': blogs})

@login_required
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blogs/blog_detail.html', {'blog': blog})

@login_required
def blog_add(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user  # Assign the logged-in user as the author
            blog.save()
            return redirect('blog')  # Redirect to the blog list page
    else:
        form = BlogForm()
    return render(request, 'blogs/blog_add.html', {'form': form})

@login_required
def blog_edit(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blogs/blog_form.html', {'form': form})

@login_required
def blog_delete(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    return render(request, 'blogs/blog_confirm_delete.html', {'blog': blog})

@login_required
def video_add(request, course_id):
    course = get_object_or_404(Course, id=course_id, trainer=request.user)  # Ensure the trainer owns the course

    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.course = course  # Link the video to the course
            video.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = VideoForm()
    return render(request, 'courses/video_form.html', {'form': form, 'course': course})

@login_required
def complete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()

    if not enrollment:
        return redirect('course_detail', course_id=course.id)

    # Check if all videos are watched
    videos = course.videos.all()

    # Generate the certificate
    certificate_path = generate_certificate(
        employee_name=request.user.get_full_name(),
        trainer_name=course.trainer.get_full_name(),
        course_name=course.title
    )

    # Serve the certificate as a downloadable file
    return FileResponse(open(certificate_path, 'rb'), as_attachment=True, filename=f'{course.title}_Certificate.png')

@login_required
def watch_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    course = video.course

    # Ensure the user is enrolled in the course
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if not enrollment:
        return redirect('course_detail', course_id=course.id)

    return render(request, 'courses/watch_video.html', {'video': video, 'course': course})


@csrf_exempt
@require_POST
@login_required
def mark_video_watched(request, video_id):
    try:
        video = Video.objects.get(id=video_id)
        # Create the watched record if it doesn't exist
        watched, created = WatchedVideo.objects.get_or_create(user=request.user, video=video)
        return JsonResponse({'status': 'success', 'watched': True})
    except Video.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Video not found'}, status=404)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('profile')
    return redirect('profile')