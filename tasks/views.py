from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .models import Task
from django.views.generic import DeleteView
from .mixins import OwnerRequiredMixin



class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'


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