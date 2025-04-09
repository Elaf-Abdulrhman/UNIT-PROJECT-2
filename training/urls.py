# urls.py (in your app)

from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Redirect to home after logout
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('complete_quiz/<int:quiz_id>/', views.complete_quiz, name='complete_quiz'),
    path('services/', views.services, name='services'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('about/', views.about, name='about'),
    path('courses/add/', views.course_add, name='course_add'),  # Add course
    path('courses/edit/<int:pk>/', views.course_edit, name='course_edit'),  # Edit course
    path('courses/delete/<int:pk>/', views.course_delete, name='course_delete'),
    path('courses/<int:course_id>/employees/', views.enrolled_employees, name='enrolled_employees'),
    path('courses/<int:course_id>/progress/', views.track_progress, name='track_progress'),
    path('courses/enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('start-course/<int:course_id>/', views.start_course, name='start_course'),
    path('courses/<int:course_id>/quiz/<str:quiz_type>/', views.show_quiz, name='take_quiz'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
