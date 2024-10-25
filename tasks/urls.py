from .views import TaskListView, TaskDetailView, TaskCreateView, CommentDeleteView, CommentUpdateView
from .views import TaskUpdateView, TaskDeleteView

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/create/', TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)