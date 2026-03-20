from django.urls import path, include
from django.contrib import admin
from . import views

app_name = "hangarin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("", views.TaskDashboardView.as_view(), name="dashboard"),
    path("task/new/", views.TaskCreateView.as_view(), name="task_create"),
    path("task/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
]
