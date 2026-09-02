import tkinter as tk
from tkinter import scrolledtext
import datetime
import json
import os
import subprocess
import shutil
import urllib.parse

HISTORY_FILE = "chat_history.json"


# =========================
# CHROME
# =========================

def open_chrome(url):
    chrome_paths = [
        os.path.expandvars(
            r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"
        ),
        os.path.expandvars(
            r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
        ),
        os.path.expandvars(
            r"%LocalAppData%\Google\Chrome\Application\chrome.exe"
        )
    ]

    chrome = shutil.which("chrome")

    if chrome:
        subprocess.Popen([chrome, url])
        return True

    for path in chrome_paths:
        if os.path.exists(path):
            subprocess.Popen([path, url])
            return True

    return False


# =========================
# ABRARAI BRAIN
# =========================

def get_response(message):

    message = message.lower().strip()

    # -------------------------
    # BASIC CHAT
    # -------------------------

    if message in ["hello", "hi", "hey", "hii", "helo"]:
        return "Hello sir! 👋 How can I help you?"

    if "your name" in message or "who are you" in message:
        return "I am AbrarAI, your personal assistant. 🤖"

    if "my name" in message:
        return "Your name is Abrar, sir."

    if "how are you" in message:
        return "I'm doing great, sir! 🤖"

    if "thank you" in message or "thanks" in message:
        return "You're welcome, sir! 😊"

    # -------------------------
    # TIME
    # -------------------------

    if "time" in message:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"Sir, the current time is {current_time} ⏰"

    # -------------------------
    # DATE
    # -------------------------

    if "date" in message or "today" in message:
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        return f"Today is {current_date} 📅"

    # -------------------------
    # GOOGLE
    # -------------------------

    if (
        "open google" in message
        or "google kholo" in message
        or "google open karo" in message
        or "google chalao" in message
    ):
        if open_chrome("https://www.google.com"):
            return "Opening Google in Chrome, sir. 🌐"
        return "Google Chrome was not found, sir."

    # -------------------------
    # YOUTUBE
    # -------------------------

    if (
        "open youtube" in message
        or "youtube kholo" in message
        or "youtube open karo" in message
        or "youtube chalao" in message
    ):
        if open_chrome("https://www.youtube.com"):
            return "Opening YouTube in Chrome, sir. ▶️"
        return "Google Chrome was not found, sir."

    # -------------------------
    # WHATSAPP
    # -------------------------

    if (
        "open whatsapp" in message
        or "whatsapp kholo" in message
        or "whatsapp open karo" in message
    ):
        if open_chrome("https://web.whatsapp.com"):
            return "Opening WhatsApp in Chrome, sir. 💬"
        return "Google Chrome was not found, sir."

    # -------------------------
    # GMAIL
    # -------------------------

    if (
        "open gmail" in message
        or "gmail kholo" in message
        or "gmail open karo" in message
    ):
        if open_chrome("https://mail.google.com"):
            return "Opening Gmail in Chrome, sir. 📧"
        return "Google Chrome was not found, sir."

    # -------------------------
    # INSTAGRAM
    # -------------------------

    if (
        "open instagram" in message
        or "instagram kholo" in message
        or "instagram open karo" in message
    ):
        if open_chrome("https://www.instagram.com"):
            return "Opening Instagram in Chrome, sir. 📸"
        return "Google Chrome was not found, sir."

    # -------------------------
    # GOOGLE SEARCH
    # -------------------------

    if message.startswith("search "):

        query = message[7:].strip()

        if query:
            search_url = (
                "https://www.google.com/search?q="
                + urllib.parse.quote_plus(query)
            )

            if open_chrome(search_url):
                return f"Searching Google for: {query} 🔎"

            return "Google Chrome was not found, sir."

    # -------------------------
    # CALCULATOR
    # -------------------------

    if (
        "calculator" in message
        or "calc" in message
    ):
        try:
            subprocess.Popen("calc.exe")
            return "Opening Calculator, sir. 🧮"
        except:
            return "I couldn't open Calculator, sir."

    # -------------------------
    # NOTEPAD
    # -------------------------

    if "notepad" in message:

        try:
            subprocess.Popen("notepad.exe")
            return "Opening Notepad, sir. 📝"
        except:
            return "I couldn't open Notepad, sir."

    # -------------------------
    # PAINT
    # -------------------------

    if "paint" in message:

        try:
            subprocess.Popen("mspaint.exe")
            return "Opening Paint, sir. 🎨"
        except:
            return "I couldn't open Paint, sir."

    # -------------------------
    # FILE EXPLORER
    # -------------------------

    if (
        "file explorer" in message
        or "explorer kholo" in message
        or "open explorer" in message
    ):

        try:
            subprocess.Popen("explorer.exe")
            return "Opening File Explorer, sir. 📁"
        except:
            return "I couldn't open File Explorer, sir."

    # -------------------------
    # CMD
    # -------------------------

    if (
        "open cmd" in message
        or "cmd kholo" in message
        or "command prompt" in message
    ):

        try:
            subprocess.Popen("cmd.exe")
            return "Opening Command Prompt, sir. 💻"
        except:
            return "I couldn't open Command Prompt, sir."

    # -------------------------
    # VS CODE
    # -------------------------

    if (
        "open vs code" in message
        or "vs code kholo" in message
        or "vscode kholo" in message
    ):

        try:
            subprocess.Popen("code")
            return "Opening VS Code, sir. 💻"
        except:
            return "I couldn't open VS Code, sir."

    # -------------------------
    # SETTINGS
    # -------------------------

    if (
        "open settings" in message
        or "settings kholo" in message
        or "settings open karo" in message
    ):

        try:
            os.system("start ms-settings:")
            return "Opening Windows Settings, sir. ⚙️"
        except:
            return "I couldn't open Windows Settings, sir."

    # -------------------------
    # UNKNOWN COMMAND
    # -------------------------

    return "I don't understand that command yet, sir. 😅"


# =========================
# SAVE CHAT
# =========================

def save_message(sender, message):

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)
    except:
        history = []

    history.append({
        "sender": sender,
        "message": message
    })

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)


# =========================
# LOAD CHAT
# =========================

def load_history():

    try:

        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)

        for item in history:

            if item["sender"] == "You":
                chat.insert(
                    tk.END,
                    "You\n" + item["message"] + "\n\n",
                    "user"
                )

            else:
                chat.insert(
                    tk.END,
                    "AbrarAI\n" + item["message"] + "\n\n",
                    "ai"
                )

    except:
        pass

    if chat.get("1.0", tk.END).strip() == "":
        chat.insert(
            tk.END,
            "AbrarAI\nHello sir! 👋 How can I help you today?\n\n",
            "ai"
        )


# =========================
# SEND MESSAGE
# =========================

def send_message(event=None):

    message = entry.get().strip()

    if not message:
        return

    chat.insert(
        tk.END,
        "You\n" + message + "\n\n",
        "user"
    )

    save_message("You", message)

    entry.delete(0, tk.END)

    response = get_response(message)

    chat.insert(
        tk.END,
        "AbrarAI\n" + response + "\n\n",
        "ai"
    )

    save_message("AbrarAI", response)

    chat.see(tk.END)


# =========================
# CLEAR CHAT
# =========================

def clear_chat():

    chat.delete("1.0", tk.END)

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump([], file)

    chat.insert(
        tk.END,
        "AbrarAI\nChat cleared. 👋\n\n",
        "ai"
    )


# =========================
# NEW CHAT
# =========================

def new_chat():

    clear_chat()

    chat.insert(
        tk.END,
        "AbrarAI\nNew chat started. How can I help you, sir?\n\n",
        "ai"
    )


# =========================
# VOICE BUTTON
# =========================

def microphone_message():

    chat.insert(
        tk.END,
        "AbrarAI\n🎤 Voice feature will be added soon, sir.\n\n",
        "ai"
    )

    chat.see(tk.END)


# =========================
# DARK MODE
# =========================

def toggle_dark_mode():

    global dark_mode

    dark_mode = not dark_mode

    if dark_mode:

        window.configure(bg="#202123")
        sidebar.configure(bg="#171717")
        main.configure(bg="#202123")
        bottom.configure(bg="#202123")

        logo.configure(
            bg="#171717",
            fg="white"
        )

        title.configure(
            bg="#202123",
            fg="white"
        )

        chat.configure(
            bg="#343541",
            fg="white",
            insertbackground="white"
        )

        entry.configure(
            bg="#40414F",
            fg="white",
            insertbackground="white"
        )

        new_chat_button.configure(
            bg="#343541",
            fg="white"
        )

        clear_button.configure(
            bg="#343541",
            fg="white"
        )

        dark_button.configure(
            bg="#343541",
            fg="white",
            text="☀ Light Mode"
        )

    else:

        window.configure(bg="white")
        sidebar.configure(bg="#F5F5F5")
        main.configure(bg="white")
        bottom.configure(bg="white")

        logo.configure(
            bg="#F5F5F5",
            fg="black"
        )

        title.configure(
            bg="white",
            fg="black"
        )

        chat.configure(
            bg="white",
            fg="black",
            insertbackground="black"
        )

        entry.configure(
            bg="white",
            fg="black",
            insertbackground="black"
        )

        new_chat_button.configure(
            bg="white",
            fg="black"
        )

        clear_button.configure(
            bg="white",
            fg="black"
        )

        dark_button.configure(
            bg="white",
            fg="black",
            text="🌙 Dark Mode"
        )


# =========================
# MAIN WINDOW
# =========================

window = tk.Tk()

window.title("AbrarAI")

window.geometry("950x650")

window.minsize(700, 500)


# =========================
# SIDEBAR
# =========================

sidebar = tk.Frame(
    window,
    width=220,
    bg="#F5F5F5"
)

sidebar.pack(
    side=tk.LEFT,
    fill=tk.Y
)

sidebar.pack_propagate(False)


logo = tk.Label(
    sidebar,
    text="🤖 AbrarAI",
    font=("Arial", 22, "bold"),
    bg="#F5F5F5"
)

logo.pack(pady=25)


new_chat_button = tk.Button(
    sidebar,
    text="＋ New Chat",
    font=("Arial", 11),
    command=new_chat
)

new_chat_button.pack(
    padx=20,
    pady=10,
    fill=tk.X
)


clear_button = tk.Button(
    sidebar,
    text="🗑 Clear Chat",
    font=("Arial", 11),
    command=clear_chat
)

clear_button.pack(
    padx=20,
    pady=10,
    fill=tk.X
)


dark_button = tk.Button(
    sidebar,
    text="🌙 Dark Mode",
    font=("Arial", 11),
    command=toggle_dark_mode
)

dark_button.pack(
    padx=20,
    pady=10,
    fill=tk.X
)


# =========================
# MAIN
# =========================

main = tk.Frame(
    window,
    bg="white"
)

main.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True
)


title = tk.Label(
    main,
    text="AbrarAI Assistant",
    font=("Arial", 20, "bold"),
    bg="white"
)

title.pack(pady=15)


# =========================
# CHAT BOX
# =========================

chat = scrolledtext.ScrolledText(
    main,
    font=("Arial", 12),
    wrap=tk.WORD,
    padx=20,
    pady=20
)

chat.pack(
    padx=20,
    pady=5,
    fill=tk.BOTH,
    expand=True
)

chat.tag_config(
    "user",
    justify="right"
)

chat.tag_config(
    "ai",
    justify="left"
)


# =========================
# INPUT
# =========================

bottom = tk.Frame(
    main,
    bg="white"
)

bottom.pack(
    padx=20,
    pady=20,
    fill=tk.X
)


entry = tk.Entry(
    bottom,
    font=("Arial", 13)
)

entry.pack(
    side=tk.LEFT,
    fill=tk.X,
    expand=True,
    ipady=12
)


send_button = tk.Button(
    bottom,
    text="Send",
    font=("Arial", 11, "bold"),
    command=send_message
)

send_button.pack(
    side=tk.RIGHT,
    ipadx=18,
    ipady=6
)


mic_button = tk.Button(
    bottom,
    text="🎤",
    font=("Arial", 14),
    command=microphone_message
)

mic_button.pack(
    side=tk.RIGHT,
    padx=8,
    ipadx=8,
    ipady=4
)


entry.bind(
    "<Return>",
    send_message
)


# =========================
# START
# =========================

load_history()

entry.focus()

window.mainloop()