from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Custom User model for Employee, Trainer roles
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('trainer', 'Trainer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    enrolled_courses = models.ManyToManyField('Course', blank=True, related_name='enrolled_users')

    def __str__(self):
        return self.username


# Course Model
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_courses'
    )
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title
        
# Enrollment Model
class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} enrolled in {self.course.title}'
