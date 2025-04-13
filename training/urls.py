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
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('services/', views.services, name='services'),
    path('reset-password-form/', auth_views.PasswordResetView.as_view(), name='reset_password_form'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('about/', views.about, name='about'),
    path('courses/add/', views.course_add, name='course_add'),  # Add course
    path('courses/edit/<int:pk>/', views.course_edit, name='course_edit'),  # Edit course
    path('courses/delete/<int:pk>/', views.course_delete, name='course_delete'),
    path('courses/<int:course_id>/employees/', views.enrolled_employees, name='enrolled_employees'),
    path('courses/enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/intro/', views.course_intro, name='course_intro'),
    path('courses/<int:course_id>/videos/add/', views.video_add, name='video_add'),
    path('courses/<int:course_id>/complete/', views.complete_course, name='complete_course'),
    path('videos/<int:video_id>/watch/', views.watch_video, name='watch_video'),
    path('videos/<int:video_id>/mark_watched/', views.mark_video_watched, name='mark_video_watched'),
    path('faq/', views.faq_view, name='faq'),
    path('blog/', views.blog_list, name='blog'),
    path('blog/add/', views.blog_add, name='blog_add'),
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blogs/', views.blog_list, name='blog_list'),  # Add this line
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
