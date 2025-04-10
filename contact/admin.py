# training/admin.py
from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')  # columns shown in the list view
    search_fields = ('name', 'email', 'subject', 'message')   # enable search
    list_filter = ('created_at',)                             # filter by date

    # Optional: make messages read-only
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')

    def has_add_permission(self, request):
        return False  # Disable adding messages manually

    def has_change_permission(self, request, obj=None):
        return False  # Disable editing messages

