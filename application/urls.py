from django.urls import path

from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, UserLoginView, RegisterPage
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # User login endpoints
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("signup/", RegisterPage.as_view(), name="signup"),

    # Tasks operations endpoints
    path("", TaskList.as_view(), name="tasks"),
    path("task/<int:pk>/", TaskDetail.as_view(), name="task"),
    path("task/create/", TaskCreate.as_view(), name="task-create"),
    path("task/edit/<int:pk>/", TaskUpdate.as_view(), name="task-edit"),
    path("task/delete/<int:pk>/", TaskDelete.as_view(), name="task-delete")
]
