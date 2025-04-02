from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_admin_view, name="register"),
    path("add_assign_task", views.add_assign_task, name="add_assign_task"),
    path("task/<int:id>", views.show_task, name="show_task")
]
