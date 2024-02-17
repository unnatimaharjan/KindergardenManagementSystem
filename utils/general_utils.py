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
