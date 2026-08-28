import os

import jwt

from datetime import datetime, timedelta, timezone

from functools import wraps

from flask import request, jsonify


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


def create_token(user_id):

    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm="HS256"
    )

    return token


def token_required(optional=False):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            auth_header = request.headers.get(
                "Authorization"
            )

            if not auth_header:

                if optional:
                    request.user_id = None
                    return function(*args, **kwargs)

                return jsonify({
                    "error": "Authorization token is required"
                }), 401

            try:

                parts = auth_header.split()

                if len(parts) != 2 or parts[0].lower() != "bearer":

                    raise ValueError("Invalid authorization header")

                token = parts[1]

                payload = jwt.decode(
                    token,
                    JWT_SECRET_KEY,
                    algorithms=["HS256"]
                )

                request.user_id = payload["user_id"]

            except jwt.ExpiredSignatureError:

                return jsonify({
                    "error": "Token has expired"
                }), 401

            except Exception:

                return jsonify({
                    "error": "Invalid authorization token"
                }), 401

            return function(*args, **kwargs)

        return wrapper

    return decorator