from django.urls import path
from .views import TaskListView, TaskDetailView, TaskCreateView
from .views import TaskUpdateView, TaskDeleteView

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/create/', TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),  # Оновлення задачі
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),  # Видалення задачі
]

