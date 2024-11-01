from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView

from .forms import TaskFilterForm, CommentForm
from .models import Task
from .mixins import OwnerRequiredMixin

from django.views.generic.edit import UpdateView, DeleteView
from .models import Comment
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import CreateView

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View


class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = self.object
            comment.author = request.user
            comment.save()
            return redirect('task_detail', pk=self.object.pk)
        return self.get(request, *args, **kwargs)


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


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_edit.html'

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        if comment.author != self.request.user:
            raise PermissionDenied  # Якщо не автор, то заборонити доступ
        return comment

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.task.pk})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        if comment.author != self.request.user:
            raise PermissionDenied  # Якщо не автор, то заборонити доступ
        return comment

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.task.pk})


class RegistrationView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
        return render(request, 'registration/register.html', {'form': form})

class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('task_list')

class CustomLogoutView(LogoutView):
    form_class = AuthenticationForm
    template_name = 'registration/logout.html'
    success_url = reverse_lazy('task_list')