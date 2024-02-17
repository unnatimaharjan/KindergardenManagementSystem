import re

import django.db.utils
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from kmsd.models import Teacher
from utils.general_utils import generate_password, get_all_teachers, validate_login_form
from utils.logging import logger


# Create your views here.
def home(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, "registration/login.html")
    rows = get_all_teachers()
    return render(request, "home.html", {"user": user, "rows": rows})


def log_in(request):
    login_template = "registration/login.html"
    if request.method == "GET":
        return render(request, login_template)
    username, password = request.POST.get("username"), request.POST.get("password")
    context = validate_login_form(username, password)
    if context:
        return render(request, login_template, context)
    user = authenticate(request, username=username, password=password)
    if not user:
        context = {"error_message": "Invalid username or password"}
        return render(request, login_template, context)
    login(request, user)
    rows = get_all_teachers()
    return render(request, "home.html", {"rows": rows})


def create_teacher(request):
    if request.method == "GET":
        return render(request, "registration/signup.html")
    email = request.POST.get("email")
    _class = request.POST.get("class")
    subject = request.POST.get("subject")
    username = re.sub("[^a-zA-Z0-9]+", "", email.split("@", 1)[0])
    password = generate_password(username)
    try:
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        teacher = Teacher(user_id=user.id, subject=subject, _class=_class)
        teacher.save()
        context = {
            "message": "User Created Successfully! Please store this safely",
            "username": username,
            "password": password,
        }
        return redirect("kmsd:home", context=context)
    except django.db.utils.IntegrityError:
        context = {"message": f"User {username} already exists!"}
        logger.exception(context)
    return redirect("kmsd:home", context=context)


def log_out(request):
    logout(request)
    return render(request, "registration/login.html")


def delete_teacher(request):
    if request.method == "GET":
        user_id = request.GET.get("id")
        user = User.objects.get(pk=user_id)
        user.delete()
    rows = get_all_teachers()
    return render(request, "home.html", {"rows": rows})
