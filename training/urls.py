# urls.py (in your app)

from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Ensure this is defined for the home page
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),  
    path('dashboard/', views.dashboard, name='dashboard'),
    path('video/<int:module_id>/', views.video_page, name='video_page'),
    path('complete_quiz/<int:quiz_id>/', views.complete_quiz, name='complete_quiz'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('about/', views.about, name='about'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/progress/<int:course_id>/', views.progress_tracking, name='progress_tracking'),
    path('courses/add/', views.course_add, name='course_add'),
    path('courses/edit/<int:pk>/', views.course_edit, name='course_edit'),
    path('courses/delete/<int:pk>/', views.course_delete, name='course_delete'),
    path('courses/<int:pk>/', views.courses, name='courses'),
]
