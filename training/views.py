from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm, CourseForm
from django.contrib.auth.decorators import login_required
from .models import Quiz, QuizResult, TrainingModule, Progress, Course  # Import Course from your models
from .forms import QuizForm  # Import QuizForm from your forms


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('home')  # Redirect to a success page or home page
    else:
        form = UserRegistrationForm()
    return render(request, 'training/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'training/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Redirect to home if the user is already logged in
        return super().dispatch(request, *args, **kwargs)

@login_required
def profile(request):
    user = request.user  # Get the logged-in user
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after saving
    else:
        form = UserRegistrationForm(instance=user)
    return render(request, 'training/profile.html', {'form': form})

def homepage(request):
    training_modules = TrainingModule.objects.all()
    return render(request, 'training/home.html', {'training_modules': training_modules})

# views.py

@login_required
def dashboard(request):
    user = request.user
    # Fetch the training modules and the user's progress on each
    training_modules = TrainingModule.objects.all()
    progress = Progress.objects.filter(user=user)
    return render(request, 'training/dashboard.html', {'training_modules': training_modules, 'progress': progress})


def video_page(request, module_id):
    module = TrainingModule.objects.get(id=module_id)
    return render(request, 'training/video_page.html', {'module': module})


@login_required
def complete_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            score = form.calculate_score()  # Add custom logic to calculate the score
            QuizResult.objects.create(user=request.user, quiz=quiz, score=score)
            return redirect('dashboard')  # Redirect after quiz completion
    else:
        form = QuizForm(quiz=quiz)  # Create a form with the quiz questions
    return render(request, 'training/complete_quiz.html', {'quiz': quiz, 'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')  # Redirect to the homepage after logout

def about(request):
    return render(request, 'training/about.html')

@login_required
def course_list(request):
    courses = Course.objects.filter(trainer=request.user)
    return render(request, 'training/course_list.html', {'courses': courses})

@login_required
def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.trainer = request.user  # Assign the logged-in user as the trainer
            course.save()
            return redirect('course_list')  # Redirect to the course list after saving
    else:
        form = CourseForm()
    return render(request, 'training/course_add.html', {'form': form})

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
    return render(request, 'training/course_form.html', {'form': form})

@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk, trainer=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'training/course_confirm_delete.html', {'course': course})

@login_required
def progress_tracking(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrolled_employees = course.enrolled_employees.all()
    return render(request, 'training/progress_tracking.html', {'course': course, 'enrolled_employees': enrolled_employees})

def home(request):
    return render(request, 'training/home.html')

def courses(request):
    courses = Course.objects.all()
    return render(request, 'training/courses.html', {'courses': courses})

def courses(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'training/course_detail.html', {'course': course})

