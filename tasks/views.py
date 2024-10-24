from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from .models import Task
from .forms import TaskForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .models import Task
from django.views.generic import DeleteView



class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'  # Використовуємо той самий шаблон, що й для створення задачі
    fields = ['title', 'description', 'status', 'priority', 'deadline', 'assigned_to']
    success_url = reverse_lazy('task_list')  # Повертаємось до списку задач після успішного оновлення

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)  # Обмежуємо доступ до задач, призначених користувачу


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)
