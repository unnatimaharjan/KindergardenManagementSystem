import re

import django.db.utils
import pandas
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from kmsd.models import Student, Teacher, Attendance
from utils.general_utils import (generate_password, get_all_students,
                                 get_all_teachers, get_user_info,
                                 post_students, set_update_profile,
                                 validate_login_form)
from utils.logging import logger


def home(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, "registration/login.html")
    rows = get_all_teachers()
    students = get_all_students()
    user_info = request.session.get("user_info")
    return render(
        request,
        "home.html",
        {"user": user, "rows": rows, "user_info": user_info, "students": students},
    )


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
    return redirect("/")


def create_teacher(request):
    if request.method == "GET":
        return render(request, "registration/signup.html")
    email, grade, subject = (
        request.POST.get("email"),
        request.POST.get("class"),
        request.POST.get("subject"),
    )
    username = re.sub(r"[^a-zA-Z0-9]+", "", email.split("@", 1)[0])
    password = generate_password(username)
    try:
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        teacher = Teacher(user_id=user.id, subject=subject, grade=grade)
        teacher.save()
        context = {
            "message": "User Created Successfully! Please store this safely",
            "username": username,
            "password": password,
        }
        request.session["user_info"] = context
        return redirect("/")
    except django.db.utils.IntegrityError:
        context = {"message": f"User {username} already exists!"}
        logger.exception(context)
    return redirect("/")


def log_out(request):
    logout(request)
    return render(request, "registration/login.html")


def delete_teacher(request):
    if request.method == "GET":
        user_id = request.GET.get("id")
        user = User.objects.get(pk=user_id)
        user.delete()
    return redirect("/")


def delete_student(request):
    if request.method == "GET":
        student_id = request.GET.get("id")
        student = Student.objects.get(pk=student_id)
        student.delete()
    return redirect("/")


def get_profile(request):
    if request.method == "POST":
        set_update_profile(request)
        return redirect("/")
    profile = get_user_info(request)
    return render(request, "profile.html", {"profile": profile})


def add_students(request):
    if request.method == "GET":
        return render(request, "upload.html")
    file = request.FILES.get("file")
    df = pandas.read_csv(file)
    post_students(df)
    return redirect("/")


def student_profile(request):
    if request.method == "GET":
        student_id = request.GET.get("id")
        attendance = Attendance.objects.select_related('student').get(student_id=student_id)
        return render(request, 'student_profile.html', {'attendance': attendance})

    if request.method == "POST":
        attendance_id = request.POST.get("attendance_id")
        attendance = Attendance.objects.get(id=attendance_id)
        attendance.grade = request.POST.get("grade")
        attendance.present_days = request.POST.get("present_days")
        attendance.save()
        return redirect("/")
