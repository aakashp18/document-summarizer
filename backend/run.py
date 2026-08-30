import os

from flask import Flask, send_from_directory
from flask_cors import CORS

from app.routes import main


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "..", "frontend")
)


app = Flask(__name__)

CORS(app)

app.register_blueprint(main)


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


if __name__ == "__main__":
    app.run(debug=True)