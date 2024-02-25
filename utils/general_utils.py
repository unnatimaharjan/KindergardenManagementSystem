import base64
import time

from django.db import connection

from kmsd.models import Student


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
            grade,
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
    id = request.GET.get("id")
    if id is None:
        query = f"""
            SELECT auth_user.id,
                first_name,
                last_name,
                email,
                subject,
                grade
                FROM auth_user INNER JOIN kmsd_teacher AS teacher
                WHERE teacher.user_id == auth_user.id AND auth_user.username='{user}';
        """
    else:
        query = f"""
            SELECT auth_user.id,
                first_name,
                last_name,
                email,
                subject,
                grade
                FROM auth_user INNER JOIN kmsd_teacher AS teacher
                WHERE teacher.user_id == auth_user.id AND auth_user.id='{id}';
        """
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            row = {
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "subject": row[4],
                "class": row[5],
            }
            return row


def set_update_profile(request):
    id, first_name, last_name, email, grade, subject = (
        request.POST.get("id", None),
        request.POST.get("first_name", ""),
        request.POST.get("last_name", ""),
        request.POST.get("email", ""),
        request.POST.get("class", ""),
        request.POST.get("subject", ""),
    )

    query = f"""
    UPDATE auth_user
    SET first_name='{first_name}', last_name='{last_name}', email='{email}'
    WHERE auth_user.id='{id}'
    RETURNING id
    """
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query)
        id = cursor.fetchone()[0]
    query = f"""
        UPDATE kmsd_teacher
        SET grade = '{grade}', subject='{subject}'
        WHERE user_id={id}
    """
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query)


def post_students(df):
    data = df.to_dict(orient="records")
    instances = [Student(**row) for row in data]
    Student.objects.bulk_create(instances)


# b'dW5uYX
def get_all_students():
    students = Student.objects.all()
    return students
