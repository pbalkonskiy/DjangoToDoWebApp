from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from application.models import Task


class TaskList(ListView):
    """Observe all over the task list and the options to view or add some new."""
    model = Task
    context_object_name = "tasks"


class TaskDetail(DetailView):
    """Take a look at one specific task from list."""
    model = Task
    context_object_name = "task"
    template_name = "application/task.html"


class TaskCreate(CreateView):
    """Call a form to create a new task in the list. Have an option to cancel."""
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("tasks")


class TaskUpdate(UpdateView):
    """Change parameters of a specific task in list."""
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("tasks")


class TaskDelete(DeleteView):
    """Deletes task from list and from table."""
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("tasks")
