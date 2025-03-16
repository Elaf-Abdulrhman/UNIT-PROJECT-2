from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    # Other URL patterns
    path('add_room/', views.add_room, name='add_room'),
    path('upload_image/', views.upload_image, name='upload_image'),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)