from django import forms
from django.forms import inlineformset_factory # Import this
from .models import Task, SubTask # Ensure SubTask is imported
from .models import Task, SubTask, Note

class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"],
        widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
    )

    class Meta:
        model = Task
        fields = ["title", "description", "deadline", "status", "priority", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Task title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Description"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }

# --- ADD THIS FORMSET BELOW ---
SubTaskFormSet = inlineformset_factory(
    Task, 
    SubTask, 
    fields=('title', 'status'), 
    extra=3,             # Number of empty subtask rows to show by default
    can_delete=False, 
    widgets={
        'title': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Subtask name'}),
        'status': forms.Select(attrs={'class': 'form-select form-select-sm'}),
    }
)

NoteFormSet = inlineformset_factory(
    Task, Note,
    fields=('content',),
    extra=1, # Just 1 empty note box by default
    widgets={'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Add a quick note...'})}
)