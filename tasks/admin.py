from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'deadline', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority', 'assigned_to')
    search_fields = ('title', 'description')
