
import json
import os
import requests

MODEL = "tinyllama:latest"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

USERS_FILE = "users.json"
HISTORY_FILE = "chat_history.json"

MAX_HISTORY = 6
DEFAULT_USER = "abrar"


# =========================
# USER FUNCTIONS
# =========================

def load_users():
    default_users = {
        "abrar": {
            "name": "Abrar"
        },
        "abbu": {
            "name": "Abbu"
        }
    }

    if not os.path.exists(USERS_FILE):
        save_users(default_users)
        return default_users

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)

        if not isinstance(users, dict):
            users = {}

    except Exception:
        users = {}

    # Make sure default profiles exist
    changed = False

    for user_id, data in default_users.items():
        if user_id not in users:
            users[user_id] = data
            changed = True

    if changed:
        save_users(users)

    return users


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def normalize_user_id(user_id):
    if not user_id:
        return DEFAULT_USER

    user_id = str(user_id).strip().lower()

    allowed = ""
    for char in user_id:
        if char.isalnum() or char in "_-":
            allowed += char

    return allowed or DEFAULT_USER


def get_display_name(user_id):
    user_id = normalize_user_id(user_id)

    users = load_users()

    if user_id not in users:
        return user_id.capitalize()

    return users[user_id].get("name", user_id.capitalize())


# =========================
# HISTORY FUNCTIONS
# =========================

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {}

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Old version was a list.
        # We reset it so users don't share old memory.
        if isinstance(data, list):
            return {}

        if not isinstance(data, dict):
            return {}

        return data

    except Exception:
        return {}


def save_history(all_history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(all_history, f, indent=4, ensure_ascii=False)


def get_user_history(user_id):
    user_id = normalize_user_id(user_id)

    all_history = load_history()

    if user_id not in all_history:
        all_history[user_id] = []

    if not isinstance(all_history[user_id], list):
        all_history[user_id] = []

    return all_history[user_id]


def save_user_history(user_id, history):
    user_id = normalize_user_id(user_id)

    all_history = load_history()

    all_history[user_id] = history[-MAX_HISTORY:]

    save_history(all_history)


# =========================
# NAME DETECTION
# =========================

def detect_name(message):
    text = message.strip()

    lower = text.lower()

    patterns = [
        "my name is ",
        "mera naam ",
        "my name's ",
        "call me "
    ]

    name = None

    for pattern in patterns:
        if pattern in lower:
            start = lower.find(pattern) + len(pattern)
            name = text[start:].strip()

            # Remove common ending words
            for ending in [" hai", " he", " h", "."]:
                if name.lower().endswith(ending):
                    name = name[:-len(ending)].strip()

            break

    if not name:
        return None

    # Keep only first part for simple names
    name = name.split(",")[0].strip()

    if not name:
        return None

    # Avoid extremely long values
    if len(name) > 40:
        return None

    return name


def update_user_name(user_id, name):
    user_id = normalize_user_id(user_id)

    users = load_users()

    if user_id not in users:
        users[user_id] = {
            "name": name
        }
    else:
        users[user_id]["name"] = name

    save_users(users)


# =========================
# IDENTITY QUESTIONS
# =========================

def is_name_question(message):
    text = message.lower().strip()

    questions = [
        "what is my name",
        "whats my name",
        "what's my name",
        "mera naam kya hai",
        "mera name kya hai",
        "my name",
        "who am i",
        "main kaun hoon",
        "mein kaun hoon"
    ]

    return any(q in text for q in questions)


# =========================
# AI
# =========================

def ask_ai(user_message, username=DEFAULT_USER):

    user_id = normalize_user_id(username)

    users = load_users()

    # Make sure selected profile exists
    if user_id not in users:
        users[user_id] = {
            "name": user_id.capitalize()
        }
        save_users(users)

    display_name = get_display_name(user_id)

    # =========================
    # NAME MEMORY
    # =========================

    detected_name = detect_name(user_message)

    if detected_name:
        update_user_name(user_id, detected_name)
        display_name = detected_name

        return f"Okay! Main aapko {display_name} bulaunga."

    # =========================
    # DIRECT NAME ANSWER
    # =========================

    if is_name_question(user_message):
        return f"Aapka naam {display_name} hai."

    # =========================
    # USER HISTORY
    # =========================

    history = get_user_history(user_id)

    history_text = ""

    for item in history[-MAX_HISTORY:]:
        role = item.get("role", "")
        content = item.get("content", "")

        if role == "user":
            history_text += f"User: {content}\n"

        elif role == "assistant":
            history_text += f"AbrarAI: {content}\n"

    # =========================
    # PROMPT
    # =========================

    prompt = f"""
You are AbrarAI, a personal AI assistant.

The current selected profile is:
Name: {display_name}
User ID: {user_id}

IMPORTANT RULES:

1. The current user's name is exactly "{display_name}".
2. Never change the user's identity based on another person's conversation.
3. Never use another profile's memory.
4. Only use the conversation history shown below.
5. If asked "What is my name?", the answer is "{display_name}".
6. Do not invent names such as Suresh, Abrar Patil, or any other person.
7. Be friendly and helpful.
8. Keep answers reasonably short.
9. You can reply in simple English or Roman Hindi/Hinglish depending on the user's message.

Conversation history for THIS USER ONLY:
{history_text}

Current user message:
{user_message}

AbrarAI:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        answer = data.get("response", "").strip()

        if not answer:
            answer = "Sorry, mujhe abhi response nahi mila."

    except requests.exceptions.ConnectionError:
        return "Ollama start nahi hai. Pehle Ollama run karo."

    except requests.exceptions.Timeout:
        return "AI response lene mein zyada time lag raha hai. Dobara try karo."

    except Exception as e:
        return f"AI ERROR: {type(e).__name__}: {e}"

    # =========================
    # SAVE ONLY THIS USER'S HISTORY
    # =========================

    history.append({
        "role": "user",
        "content": user_message
    })

    history.append({
        "role": "assistant",
        "content": answer
    })

    save_user_history(user_id, history)

    return answer


# =========================
# CLI TEST
# =========================

if __name__ == "__main__":

    print("================================")
    print("       AbrarAI CLI")
    print("================================")
    print("Type 'switch' to change profile.")
    print("Type 'exit' to quit.\n")

    current_user = DEFAULT_USER

    print(f"Current profile: {get_display_name(current_user)}")

    while True:

        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("AbrarAI: Bye!")
            break

        if user_input.lower() == "switch":

            users = load_users()

            print("\nAvailable profiles:")

            for user_id, data in users.items():
                print(f"- {user_id} ({data.get('name', user_id)})")

            selected = input("\nEnter profile ID: ").strip().lower()

            if selected in users:
                current_user = selected
                print(
                    f"AbrarAI: Switched to "
                    f"{get_display_name(current_user)}."
                )
            else:
                print("AbrarAI: Profile nahi mila.")

            continue

        answer = ask_ai(user_input, current_user)

        print(f"AbrarAI: {answer}")