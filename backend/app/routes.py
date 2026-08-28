import os

from flask import Blueprint, request, jsonify

from app.services.document_service import extract_text_from_file
from app.services.image_service import summarize_image
from app.services.summarizer_service import summarize_text
from app.services.auth_service import register_user, login_user
from app.auth import create_token
from app.auth import token_required
from app.database import get_db_connection


main = Blueprint("main", __name__)


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


ALLOWED_DOCUMENTS = [".pdf", ".docx", ".txt"]
ALLOWED_IMAGES = [".jpg", ".jpeg", ".png"]



# TEST


@main.route("/test", methods=["GET"])
def test():

    return jsonify({
        "message": "Backend is working"
    })










# ========================================
# REGISTER
# ========================================

@main.route("/register", methods=["POST"])
def register():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400

        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")

        if not username:
            return jsonify({
                "error": "Username is required"
            }), 400

        if not email:
            return jsonify({
                "error": "Email is required"
            }), 400

        if not password:
            return jsonify({
                "error": "Password is required"
            }), 400

        result, status_code = register_user(
            username,
            email,
            password
        )

        return jsonify(result), status_code

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ========================================
# LOGIN
# ========================================

@main.route("/login", methods=["POST"])
def login():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400

        login = data.get("login", "").strip()
        password = data.get("password", "")

        if not login:
            return jsonify({
                "error": "Username or email is required"
            }), 400

        if not password:
            return jsonify({
                "error": "Password is required"
            }), 400

        result, status_code = login_user(
            login,
            password
        )

        if status_code != 200:
            return jsonify(result), status_code

        user_id = result["user"]["id"]

        token = create_token(user_id)

        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": result["user"]
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ========================================
# SUMMARIZE TEXT
# ========================================

@main.route("/summarize-text", methods=["POST"])
@token_required(optional=True)
def summarize_text_route():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400

        text = data.get("text", "")

        if not text.strip():
            return jsonify({
                "error": "Text is required"
            }), 400

        summary = summarize_text(text)

        # ========================================
        # SAVE HISTORY ONLY IF USER IS LOGGED IN
        # ========================================

        if request.user_id is not None:

            connection = get_db_connection()

            try:

                with connection.cursor() as cursor:

                    cursor.execute(
                        """
                        INSERT INTO document_history
                        (
                            user_id,
                            filename,
                            file_type,
                            summary_type,
                            summary
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            request.user_id,
                            "Entered Text",
                            "text",
                            "text",
                            summary
                        )
                    )

                    connection.commit()

            finally:

                connection.close()

        return jsonify({
            "summary": summary
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ========================================
# SUMMARIZE DOCUMENT
# ========================================

@main.route("/summarize-file", methods=["POST"])
@token_required(optional=True)
def summarize_file():

    try:

        if "file" not in request.files:

            return jsonify({
                "error": "No file uploaded"
            }), 400

        file = request.files["file"]

        if file.filename == "":

            return jsonify({
                "error": "No file selected"
            }), 400

        extension = os.path.splitext(
            file.filename
        )[1].lower()

        if extension not in ALLOWED_DOCUMENTS:

            return jsonify({
                "error": "Only PDF, DOCX and TXT files are allowed"
            }), 400

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(file_path)

        text = extract_text_from_file(file_path)

        if not text:

            return jsonify({
                "error": "Could not extract text from document"
            }), 400

        summary = summarize_text(text)

        # ========================================
        # SAVE HISTORY ONLY IF USER IS LOGGED IN
        # ========================================

        if request.user_id is not None:

            connection = get_db_connection()

            try:

                with connection.cursor() as cursor:

                    cursor.execute(
                        """
                        INSERT INTO document_history
                        (
                            user_id,
                            filename,
                            file_type,
                            summary_type,
                            summary
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            request.user_id,
                            file.filename,
                            extension.replace(".", ""),
                            "document",
                            summary
                        )
                    )

                    connection.commit()

            finally:

                connection.close()

        return jsonify({
            "filename": file.filename,
            "summary": summary
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ========================================
# SUMMARIZE IMAGE
# ========================================

@main.route("/summarize-image", methods=["POST"])
@token_required(optional=True)
def summarize_image_route():

    try:

        if "file" not in request.files:

            return jsonify({
                "error": "No image uploaded"
            }), 400

        file = request.files["file"]

        if file.filename == "":

            return jsonify({
                "error": "No image selected"
            }), 400

        extension = os.path.splitext(
            file.filename
        )[1].lower()

        if extension not in ALLOWED_IMAGES:

            return jsonify({
                "error": "Only JPG, JPEG and PNG images are allowed"
            }), 400

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(file_path)

        summary = summarize_image(file_path)

        # ========================================
        # SAVE HISTORY ONLY IF USER IS LOGGED IN
        # ========================================

        if request.user_id is not None:

            connection = get_db_connection()

            try:

                with connection.cursor() as cursor:

                    cursor.execute(
                        """
                        INSERT INTO document_history
                        (
                            user_id,
                            filename,
                            file_type,
                            summary_type,
                            summary
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            request.user_id,
                            file.filename,
                            extension.replace(".", ""),
                            "picture",
                            summary
                        )
                    )

                    connection.commit()

            finally:

                connection.close()

        return jsonify({
            "filename": file.filename,
            "summary": summary
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ========================================
# GET USER HISTORY
# ========================================

@main.route("/history", methods=["GET"])
@token_required()
def get_history():

    try:

        connection = get_db_connection()

        try:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        filename,
                        file_type,
                        summary_type,
                        summary,
                        created_at
                    FROM document_history
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                    """,
                    (request.user_id,)
                )

                rows = cursor.fetchall()

                history = []

                for row in rows:

                    history.append({
                        "id": row[0],
                        "filename": row[1],
                        "file_type": row[2],
                        "summary_type": row[3],
                        "summary": row[4],
                        "created_at": row[5].isoformat()
                        if row[5] else None
                    })

                return jsonify({
                    "history": history
                }), 200

        finally:

            connection.close()

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500