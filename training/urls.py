# urls.py (in your app)

from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),  # Use the custom logout view
    path('dashboard/', views.dashboard, name='dashboard'),
    path('video/<int:module_id>/', views.video_page, name='video_page'),
    path('complete_quiz/<int:quiz_id>/', views.complete_quiz, name='complete_quiz'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('about/', views.about, name='about'),
]
