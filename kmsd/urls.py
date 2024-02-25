from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="root"),
    path("home/", views.home, name="home"),
    path("login/", views.log_in, name="login"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.create_teacher, name="signup"),
    path("delete_user/", views.delete_teacher, name="delete"),
    path("profile/", views.get_profile, name="profile"),
    path("add_students/", views.add_students, name="add_students"),
]
app_name = "kmsd"
