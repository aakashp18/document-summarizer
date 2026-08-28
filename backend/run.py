from flask import Flask, send_from_directory

from app.routes import main
from flask_cors import CORS


app = Flask(__name__)

CORS(app)


app.register_blueprint(main)


@app.route("/")
def home():
    return send_from_directory(
        "../frontend/pages",
        "login.html"
    )


@app.route("/pages/<path:filename>")
def pages(filename):
    return send_from_directory(
        "../frontend/pages",
        filename
    )


@app.route("/js/<path:filename>")
def javascript(filename):
    return send_from_directory(
        "../frontend/js",
        filename
    )


@app.route("/css/<path:filename>")
def css(filename):
    return send_from_directory(
        "../frontend/css",
        filename
    )


if __name__ == "__main__":
    app.run(debug=True)