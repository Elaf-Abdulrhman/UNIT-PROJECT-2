from django.contrib import admin
from .models import Course, Video

# Define VideoInline first
class VideoInline(admin.TabularInline):
    model = Video
    extra = 1  # Allows the admin to add multiple videos directly to the course.

# Now define the CourseAdmin
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'trainer', 'start_date', 'end_date')
    list_filter = ('trainer', 'start_date')
    search_fields = ('title', 'description')
    inlines = [VideoInline]  # This will work now that VideoInline is defined

# Register models with the admin
admin.site.register(Course, CourseAdmin)
admin.site.register(Video)
