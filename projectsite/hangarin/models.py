from django.db import models
from django.utils import timezone
from django.conf import settings # Required for User link
from datetime import timedelta

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Priority(BaseModel):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Priorities"
    def __str__(self):
        return self.name

class Category(BaseModel):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name

class Task(BaseModel):
    # LINK TO USER - This is the critical change
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    @property
    def completion_percent(self):
        if self.status == "Completed": return 100
        subtasks = self.subtasks.all()
        if subtasks.exists():
            completed = subtasks.filter(status="Completed").count()
            return round(100 * completed / subtasks.count()) if subtasks.count() else 0
        return 50 if self.status == "In Progress" else 0

    @property
    def progress_bar_color(self):
        p = self.completion_percent
        if p < 30: return "danger"
        if p <= 70: return "warning"
        return "success"

    @property
    def is_due_soon(self):
        if not self.deadline: return False
        now = timezone.now()
        return now <= self.deadline <= now + timedelta(hours=48)

    def __str__(self):
        return self.title

class SubTask(BaseModel):
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=Task.STATUS_CHOICES, default="Pending")

class Note(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="notes")
    content = models.TextField()
