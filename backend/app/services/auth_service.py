from werkzeug.security import generate_password_hash, check_password_hash

from app.database import get_db_connection
import re

def is_valid_email(email):

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return re.match(pattern, email) is not None


def register_user(username, email, password):

    if not is_valid_email(email):

     return {
        "error": "Please enter a valid email address"
    }, 400

    connection = get_db_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE username = %s OR email = %s
                """,
                (username, email)
            )

            existing_user = cursor.fetchone()

            if existing_user:
                return {
                    "error": "Username or email already exists"
                }, 409

            hashed_password = generate_password_hash(password)

            cursor.execute(
                """
                INSERT INTO users
                (username, email, password)
                VALUES (%s, %s, %s)
                """,
                (username, email, hashed_password)
            )

            connection.commit()

            return {
                "message": "User registered successfully"
            }, 201

    finally:

        connection.close()


def login_user(login, password):

    connection = get_db_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id, username, email, password
                FROM users
                WHERE username = %s OR email = %s
                """,
                (login, login)
            )

            user = cursor.fetchone()

            if not user:

                return {
                    "error": "Invalid username/email or password"
                }, 401

            user_id = user[0]
            username = user[1]
            user_email = user[2]
            hashed_password = user[3]

            if not check_password_hash(
                hashed_password,
                password
            ):

                return {
                    "error": "Invalid username/email or password"
                }, 401

            return {
                "message": "Login successful",
                "user": {
                    "id": user_id,
                    "username": username,
                    "email": user_email
                }
            }, 200

    finally:

        connection.close()






