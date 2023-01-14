from django.shortcuts import redirect

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from application.models import Task


class UserLoginView(LoginView):
    template_name = "application/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("tasks")


class RegisterPage(FormView):
    template_name = "application/signup.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        """
        Redirects the user ones the signup form is submitted. We make sure that user is logged in.
        Triggered ones the POST-request to a signup sent.
        """
        user = form.save()
        if user:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        """To redirect the authenticated user to the tasks list from the signup page."""
        if self.request.user.is_authenticated:
            return redirect("tasks")
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    """Observe all over the task list and the options to add some new or search from list."""
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

        # The search bar for tasks titles realization.
        search_input = self.request.GET.get("search-area") or ""
        if search_input:
            context["tasks"] = context["tasks"].filter(title__startswith=search_input)
        context["search_input"] = search_input
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
