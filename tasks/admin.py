from django.contrib import admin
from .models import Task, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class TaskAdmin(admin.ModelAdmin):
    inlines = [CommentInline]

admin.site.register(Task, TaskAdmin)
admin.site.register(Comment)
