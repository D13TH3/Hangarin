from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse_lazy
from datetime import timedelta
from .models import Task, Category
from .forms import TaskForm, SubTaskFormSet, NoteFormSet 

class TaskDashboardView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "hangarin/dashboard.html"
    context_object_name = "tasks"
    paginate_by = 20

    def get_queryset(self):
        # SECURITY: Only show tasks for the logged-in user
        qs = Task.objects.filter(user=self.request.user).select_related("priority", "category").prefetch_related("subtasks", "notes").order_by("-created_at")
        search = self.request.GET.get("search", "").strip()
        if search:
            qs = qs.filter(title__icontains=search)
        category_id = self.request.GET.get("category", "")
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        total = qs.count()
        completed = qs.filter(status="Completed").count()
        
        # Data for your colored cards
        context["total_tasks"] = total
        context["completed_tasks"] = completed
        context["efficiency_score"] = round((completed / total * 100), 1) if total else 0
        
        now = timezone.now()
        context["due_soon_count"] = qs.filter(
            deadline__gte=now, deadline__lte=now + timedelta(hours=48)
        ).count()
        
        context["categories"] = Category.objects.all().order_by("name")
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "hangarin/task_form.html"
    success_url = reverse_lazy("hangarin:dashboard")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['subtasks'] = SubTaskFormSet(self.request.POST)
            data['notes'] = NoteFormSet(self.request.POST)
        else:
            data['subtasks'] = SubTaskFormSet()
            data['notes'] = NoteFormSet() 
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        subtasks = context['subtasks']
        notes = context['notes']
        
        # Link the task to the logged-in user automatically
        form.instance.user = self.request.user 
    
        if subtasks.is_valid() and notes.is_valid():
            self.object = form.save()
            subtasks.instance = self.object
            subtasks.save()
            notes.instance = self.object
            notes.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("hangarin:dashboard")
    template_name = "hangarin/task_confirm_delete.html"
