from flask import Flask, request, jsonify, send_from_directory, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from ai_brain import ask_ai
from ppt_generator import create_ppt
import sqlite3
import os


# =========================================================
# ABRARAI SERVER
# =========================================================

app = Flask(
    __name__,
    static_folder="website"
)

app.secret_key = "abrarai-secret-key-change-later"

DATABASE = "users.db"


# =========================================================
# DATABASE
# =========================================================

def get_db():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
    """)

    conn.commit()

    conn.close()


init_db()


# =========================================================
# WEBSITE
# =========================================================

@app.route("/")
def home():

    return send_from_directory(
        "website",
        "index.html"
    )


@app.route("/<path:path>")
def static_files(path):

    return send_from_directory(
        "website",
        path
    )


# =========================================================
# SIGNUP
# =========================================================

@app.route(
    "/api/signup",
    methods=["POST"]
)
def signup():

    data = request.get_json()

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )

    if not email or not password:

        return jsonify({
            "success": False,
            "message": "Email aur password required hai."
        }), 400


    if len(password) < 6:

        return jsonify({
            "success": False,
            "message": "Password kam se kam 6 characters ka hona chahiye."
        }), 400


    conn = get_db()

    existing_user = conn.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    ).fetchone()


    if existing_user:

        conn.close()

        return jsonify({
            "success": False,
            "message": "Ye email already registered hai."
        }), 409


    password_hash = generate_password_hash(
        password
    )


    conn.execute(
        """
        INSERT INTO users
        (email, password)
        VALUES (?, ?)
        """,
        (
            email,
            password_hash
        )
    )

    conn.commit()

    conn.close()


    return jsonify({
        "success": True,
        "message": "Account successfully create ho gaya."
    })


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/api/login",
    methods=["POST"]
)
def login():

    data = request.get_json()

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )


    if not email or not password:

        return jsonify({
            "success": False,
            "message": "Email aur password required hai."
        }), 400


    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    conn.close()


    if (
        not user
        or not check_password_hash(
            user["password"],
            password
        )
    ):

        return jsonify({
            "success": False,
            "message": "Email ya password galat hai."
        }), 401


    session["user_id"] = user["id"]

    session["email"] = user["email"]


    return jsonify({

        "success": True,

        "message": "Login successful!",

        "email": user["email"]

    })


# =========================================================
# LOGOUT
# =========================================================

@app.route(
    "/api/logout",
    methods=["POST"]
)
def logout():

    session.clear()

    return jsonify({
        "success": True,
        "message": "Logout successful."
    })


# =========================================================
# CURRENT USER
# =========================================================

@app.route(
    "/api/me",
    methods=["GET"]
)
def current_user():

    if "user_id" not in session:

        return jsonify({
            "logged_in": False
        })


    return jsonify({

        "logged_in": True,

        "user_id": session["user_id"],

        "email": session["email"]

    })


# =========================================================
# AI CHAT
# =========================================================

@app.route(
    "/api/chat",
    methods=["POST"]
)
def chat():

    # Login required

    if "user_id" not in session:

        return jsonify({
            "response": "Pehle login karo sir."
        }), 401


    data = request.get_json()


    if not data or "message" not in data:

        return jsonify({
            "response": "Message nahi mila sir."
        }), 400


    message = data["message"].strip()


    if not message:

        return jsonify({
            "response": "Please kuch message likho."
        }), 400


    user_id = session.get(
        "user_id"
    )


    try:

        response = ask_ai(

            message,

            user_id=user_id

        )


        return jsonify({
            "response": response
        })


    except Exception as e:

        print(
            "AI ERROR:",
            e
        )


        return jsonify({
            "response":
                "Sorry sir, AI mein kuch problem aa gayi."
        }), 500


# =========================================================
# PPT GENERATOR
# =========================================================

@app.route(
    "/api/ppt",
    methods=["POST"]
)
def generate_ppt():

    # Login required

    if "user_id" not in session:

        return jsonify({

            "success": False,

            "message": "Pehle login karo sir."

        }), 401


    data = request.get_json()


    if not data:

        return jsonify({

            "success": False,

            "message": "PPT data nahi mila."

        }), 400


    topic = data.get(
        "topic",
        ""
    ).strip()


    slides = data.get(
        "slides",
        10
    )


    if not topic:

        return jsonify({

            "success": False,

            "message": "PPT topic required hai."

        }), 400


    try:

        slides = int(slides)

    except:

        slides = 10


    if slides < 1:

        slides = 1


    if slides > 30:

        slides = 30


    try:

        filepath = create_ppt(

            topic,

            slides

        )


        filename = os.path.basename(
            filepath
        )


        return jsonify({

            "success": True,

            "message":
                "PPT successfully created!",

            "file":
                filepath,

            "filename":
                filename

        })


    except Exception as e:

        print(
            "PPT ERROR:",
            e
        )


        return jsonify({

            "success": False,

            "message":
                "PPT generate nahi ho payi."

        }), 500


# =========================================================
# PPT DOWNLOAD
# =========================================================

@app.route(
    "/api/ppt/download",
    methods=["GET"]
)
def download_ppt():

    if "user_id" not in session:

        return jsonify({

            "success": False,

            "message":
                "Pehle login karo sir."

        }), 401


    filename = request.args.get(
        "file",
        ""
    )


    if not filename:

        return jsonify({

            "success": False,

            "message":
                "PPT file nahi mili."

        }), 400


    filepath = os.path.join(

        "generated_ppts",

        os.path.basename(filename)

    )


    if not os.path.exists(filepath):

        return jsonify({

            "success": False,

            "message":
                "PPT file exist nahi karti."

        }), 404


    return send_file(

        filepath,

        as_attachment=True,

        download_name=os.path.basename(
            filepath
        )

    )


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    print("================================")

    print(
        "       ABRARAI SERVER"
    )

    print("================================")

    print(
        "Website: http://127.0.0.1:5000"
    )

    print(
        "Database: users.db"
    )

    print(
        "PPT Generator: ON"
    )

    print(
        "AI Chat: ON"
    )

    print(
        "Server starting..."
    )

    print("================================")


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )