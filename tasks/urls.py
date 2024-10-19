from django.urls import path
from .views import TaskListView, TaskDetailView, TaskCreateView

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),  # Перегляд списку задач
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),  # Перегляд детальної інформації
    path('task/create/', TaskCreateView.as_view(), name='task_create'),  # Створення задачі
]
