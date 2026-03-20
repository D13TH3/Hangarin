from django.contrib import admin
from .models import Priority, Category, Task, SubTask, Note

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Display: title, status, deadline, priority, category
    list_display = ('title', 'status', 'deadline', 'priority', 'category')
    # Filters: status, priority, category
    list_filter = ('status', 'priority', 'category')
    # Search: title, description
    search_fields = ('title', 'description')

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    # Display: title, status, and custom parent_task_name
    list_display = ('title', 'status', 'parent_task_name')
    # Filter: status
    list_filter = ('status',)
    # Search: title
    search_fields = ('title',)

    # Custom field to show the Parent Task's title
    def parent_task_name(self, obj):
        return obj.parent_task.title
    parent_task_name.short_description = 'Parent Task'

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    # Display: task, content, and created_at
    list_display = ('task', 'content', 'created_at')
    # Filter: created_at
    list_filter = ('created_at',)
    # Search: content
    search_fields = ('content',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
