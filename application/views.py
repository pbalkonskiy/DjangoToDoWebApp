from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from application.models import Task


class UserLoginView(LoginView):
    template_name = "application/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("tasks")


class TaskList(LoginRequiredMixin, ListView):
    """Observe all over the task list and the options to view or add some new."""
    model = Task
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        """
        Method ensures that the user receives only the information from the task list,
        that he directly entered, with help of overriding mixins context data method.
        """
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        context["count"] = context["tasks"].filter(complete=False).count()
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    """Take a look at one specific task from list."""
    model = Task
    context_object_name = "task"
    template_name = "application/task.html"


class TaskCreate(LoginRequiredMixin, CreateView):
    """Call a form to create a new task in the list. Have an option to cancel."""
    model = Task
    fields = ["title",
              "description",
              "complete"]
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        """To separate quarry sets from different users."""
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    """Change parameters of a specific task in list."""
    model = Task
    fields = ["title",
              "description",
              "complete"]
    success_url = reverse_lazy("tasks")


class TaskDelete(LoginRequiredMixin, DeleteView):
    """Deletes task from list and from table."""
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("tasks")
