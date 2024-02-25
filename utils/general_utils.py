import base64
import time

from django.db import connection


def validate_login_form(username, password):
    if not username and not password:
        return {"error_message": "Username and Password is required."}
    if not username:
        return {"error_message": "Username is required"}
    if not password:
        return {"error_message": "Password is required"}


def generate_password(username):
    current_time = time.time()
    new_username = username + str(int(current_time))
    new_username = new_username.encode("utf-8")
    new_username = base64.b64encode(new_username)
    password = str(new_username)[:8]
    return password


def get_all_teachers():
    query = """
            SELECT auth_user.id,
            username,
            first_name,
            last_name,
            email,
            subject,
            _class,
            password
            FROM auth_user INNER JOIN kmsd_teacher AS teacher
            WHERE teacher.user_id == auth_user.id AND is_superuser == 0;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows


def get_user_info(request):
    user = request.user
    query = f"""
        SELECT auth_user.id,
            first_name,
            last_name,
            email,
            subject,
            _class
            FROM auth_user INNER JOIN kmsd_teacher AS teacher
            WHERE teacher.user_id == auth_user.id AND auth_user.username='{user}';
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
        row = {
            "first_name": row[1],
            "last_name": row[2],
            "email": row[3],
            "subject": row[4],
            "class": row[5],
        }
        return row


def set_update_profile(request):
    first_name, last_name, email, _class, subject = (
        request.POST.get("first_name", ""),
        request.POST.get("last_name", ""),
        request.POST.get("email", ""),
        request.POST.get("class", ""),
        request.POST.get("subject", ""),
    )
    query = f"""
    UPDATE auth_user
    SET first_name = '{first_name}', last_name = '{last_name}', email = '{email}'
    WHERE auth_user.username = '{request.user}'
    RETURNING id
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        id = cursor.fetchone()[0]
    query = f"""
        UPDATE kmsd_teacher
        SET _class = '{_class}', subject='{subject}'
        WHERE id={id}
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
