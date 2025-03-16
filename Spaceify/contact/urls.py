from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'contact'

urlpatterns = [
    path('contact_us/', views.contact_us, name='contact_us'),
]