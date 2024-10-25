from django.db import models
from django.contrib.auth.models import User



class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=255)  # Назва завдання
    description = models.TextField(blank=True, null=True)  # Опис завдання
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')  # Статус
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')  # Пріоритет
    deadline = models.DateTimeField(null=True, blank=True)  # Термін виконання
    created_at = models.DateTimeField(auto_now_add=True)  # Дата створення
    updated_at = models.DateTimeField(auto_now=True)  # Дата оновлення
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Відповідальний користувач

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='comments/', blank=True, null=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.task.title}'