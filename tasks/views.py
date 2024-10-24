from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from .forms import TaskFilterForm
from .models import Task
from django.views.generic import DeleteView
from .mixins import OwnerRequiredMixin



class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Фильтрация по параметрам GET запроса
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем форму фильтрации в контекст
        context['filter_form'] = TaskFilterForm(self.request.GET or None)
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'status', 'priority', 'deadline', 'assigned_to']
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.assigned_to = self.request.user
        return super().form_valid(form)



class TaskUpdateView(OwnerRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'status', 'priority', 'deadline', 'assigned_to']
    success_url = reverse_lazy('task_list')

class TaskDeleteView(OwnerRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')