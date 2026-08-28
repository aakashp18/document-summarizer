import os

from flask import Flask, send_from_directory
from flask_cors import CORS

from app.routes import main


# ========================================
# PATHS
# ========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_DIR = os.path.dirname(BASE_DIR)

FRONTEND_DIR = os.path.join(
    PROJECT_DIR,
    "frontend"
)


# ========================================
# FLASK APP
# ========================================

app = Flask(__name__)

CORS(app)


# ========================================
# REGISTER ROUTES
# ========================================

app.register_blueprint(main)


# ========================================
# FRONTEND
# ========================================

@app.route("/")
def home():

    return send_from_directory(
        os.path.join(FRONTEND_DIR, "pages"),
        "login.html"
    )


@app.route("/pages/<path:filename>")
def pages(filename):

    return send_from_directory(
        os.path.join(FRONTEND_DIR, "pages"),
        filename
    )


@app.route("/js/<path:filename>")
def javascript(filename):

    return send_from_directory(
        os.path.join(FRONTEND_DIR, "js"),
        filename
    )


@app.route("/css/<path:filename>")
def css(filename):

    return send_from_directory(
        os.path.join(FRONTEND_DIR, "css"),
        filename
    )


# ========================================
# RUN LOCALLY
# ========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )