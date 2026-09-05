
from flask import Flask, request, jsonify, send_from_directory, session
from ai_brain import ask_ai, load_users, get_display_name
import re

app = Flask(__name__)

# Session ke liye secret key
app.secret_key = "abrarai-secret-key-change-this-later"


# =========================
# WEBSITE
# =========================

@app.route("/")
def home():
    return send_from_directory("website", "index.html")


# =========================
# GET ALL USERS
# =========================

@app.route("/api/users", methods=["GET"])
def get_users():
    users = load_users()

    profiles = []

    for user_id, user_data in users.items():
        profiles.append({
            "id": user_id,
            "name": get_display_name(user_id)
        })

    return jsonify({
        "success": True,
        "users": profiles
    })


# =========================
# SELECT USER
# =========================

@app.route("/api/select-user", methods=["POST"])
def select_user():

    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id", "").strip().lower()

    users = load_users()

    if not user_id:
        return jsonify({
            "success": False,
            "error": "User ID missing"
        }), 400

    if user_id not in users:
        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404

    session["user_id"] = user_id

    return jsonify({
        "success": True,
        "user_id": user_id,
        "name": get_display_name(user_id)
    })


# =========================
# CURRENT USER
# =========================

@app.route("/api/current-user", methods=["GET"])
def current_user():

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "success": False,
            "logged_in": False
        })

    return jsonify({
        "success": True,
        "logged_in": True,
        "user_id": user_id,
        "name": get_display_name(user_id)
    })


# =========================
# ADD NEW PROFILE
# =========================

@app.route("/api/add-user", methods=["POST"])
def add_user():

    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    user_id = data.get("user_id", "").strip().lower()

    # Name check
    if not name:
        return jsonify({
            "success": False,
            "error": "Name is required"
        }), 400

    # Agar ID nahi diya toh name se automatically ID banao
    if not user_id:
        user_id = name.lower()
        user_id = re.sub(r"[^a-z0-9_]+", "_", user_id)
        user_id = user_id.strip("_")

    # ID valid hai ya nahi
    if not re.match(r"^[a-z0-9_]+$", user_id):
        return jsonify({
            "success": False,
            "error": "Profile ID sirf letters, numbers aur underscore use kare"
        }), 400

    users = load_users()

    # Duplicate profile check
    if user_id in users:
        return jsonify({
            "success": False,
            "error": "Ye profile already exist karti hai"
        }), 409

    # New profile create
    users[user_id] = {
        "name": name
    }

    # users.json save
    import json

    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

    # Automatically new profile select
    session["user_id"] = user_id

    return jsonify({
        "success": True,
        "user_id": user_id,
        "name": name
    })


# =========================
# CHAT
# =========================

@app.route("/api/chat", methods=["POST"])
def chat():

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "success": False,
            "error": "Please select a profile first"
        }), 401

    data = request.get_json(silent=True) or {}

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "success": False,
            "error": "Message empty hai"
        }), 400

    try:

        reply = ask_ai(user_message, user_id)

        return jsonify({
            "success": True,
            "reply": reply
        })

    except Exception as e:

        print("AI ERROR:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================
# LOGOUT / CHANGE PROFILE
# =========================

@app.route("/api/logout", methods=["POST"])
def logout():

    session.pop("user_id", None)

    return jsonify({
        "success": True
    })


# =========================
# START SERVER
# =========================

if __name__ == "__main__":

    print("")
    print("================================")
    print("       AbrarAI Web Started")
    print("================================")
    print("Local:   http://127.0.0.1:5000")
    print("Network: http://0.0.0.0:5000")
    print("================================")
    print("")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
