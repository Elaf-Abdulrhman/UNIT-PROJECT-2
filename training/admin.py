from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'trainer', 'start_date', 'end_date')
    list_filter = ('trainer', 'start_date')
    search_fields = ('title', 'description')
