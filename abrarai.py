
import tkinter as tk
from tkinter import scrolledtext
import webbrowser
from datetime import datetime

from ai_brain import ask_ai


# =========================
# ABRARAI RESPONSE
# =========================

def get_response(message):
    message = message.strip()

    if not message:
        return "Sir, kuch type karo."

    # Open websites
    if message.lower() in ["open google", "google kholo", "google open karo"]:
        webbrowser.open("https://www.google.com")
        return "Opening Google, sir. 🌐"

    if message.lower() in ["open youtube", "youtube kholo", "youtube open karo"]:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube, sir. ▶️"

    if message.lower() in ["open whatsapp", "whatsapp kholo"]:
        webbrowser.open("https://web.whatsapp.com")
        return "Opening WhatsApp, sir. 💬"

    if message.lower() in ["open instagram", "instagram kholo"]:
        webbrowser.open("https://www.instagram.com")
        return "Opening Instagram, sir. 📸"

    if message.lower() in ["open gmail", "gmail kholo"]:
        webbrowser.open("https://mail.google.com")
        return "Opening Gmail, sir. 📧"

    # Search Google
    if message.lower().startswith("search "):
        query = message[7:].strip()

        if query:
            webbrowser.open(
                "https://www.google.com/search?q="
                + query.replace(" ", "+")
            )
            return f"Searching Google for {query}, sir. 🔎"

    # Time
    if message.lower() in ["time", "what is the time", "time kya hai"]:
        return datetime.now().strftime("Sir, the time is %I:%M %p. ⏰")

    # Date
    if message.lower() in ["date", "today date", "aaj ki date kya hai"]:
        return datetime.now().strftime(
            "Sir, today's date is %d %B %Y. 📅"
        )

    # Everything else → AI Brain
    return ask_ai(message)


# =========================
# SEND MESSAGE
# =========================

def send_message(event=None):
    message = user_input.get().strip()

    if not message:
        return

    # Show user message
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"You: {message}\n", "user")
    chat_box.config(state=tk.DISABLED)

    user_input.delete(0, tk.END)

    # Get AI response
    try:
        response = get_response(message)
    except Exception as e:
        response = f"Sorry sir, error aa gaya:\n{e}"

    # Show AI response
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"AbrarAI: {response}\n\n", "ai")
    chat_box.config(state=tk.DISABLED)

    chat_box.see(tk.END)


# =========================
# CLEAR CHAT
# =========================

def clear_chat():
    chat_box.config(state=tk.NORMAL)
    chat_box.delete("1.0", tk.END)
    chat_box.config(state=tk.DISABLED)


# =========================
# NEW CHAT
# =========================

def new_chat():
    clear_chat()

    chat_box.config(state=tk.NORMAL)
    chat_box.insert(
        tk.END,
        "AbrarAI: New chat started, sir. 🤖\n\n",
        "ai"
    )
    chat_box.config(state=tk.DISABLED)


# =========================
# DARK MODE
# =========================

dark_mode = True


def toggle_theme():
    global dark_mode

    if dark_mode:
        root.configure(bg="#f2f2f2")
        title_label.configure(bg="#f2f2f2", fg="#111111")
        chat_box.configure(
            bg="white",
            fg="black",
            insertbackground="black"
        )
        user_input.configure(
            bg="white",
            fg="black",
            insertbackground="black"
        )
        send_button.configure(
            bg="#dddddd",
            fg="black"
        )
        theme_button.configure(
            bg="#dddddd",
            fg="black",
            text="🌙 Dark Mode"
        )

        dark_mode = False

    else:
        root.configure(bg="#111111")
        title_label.configure(bg="#111111", fg="white")
        chat_box.configure(
            bg="#181818",
            fg="white",
            insertbackground="white"
        )
        user_input.configure(
            bg="#222222",
            fg="white",
            insertbackground="white"
        )
        send_button.configure(
            bg="#333333",
            fg="white"
        )
        theme_button.configure(
            bg="#333333",
            fg="white",
            text="☀️ Light Mode"
        )

        dark_mode = True


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title("AbrarAI")
root.geometry("850x650")
root.minsize(650, 500)

root.configure(bg="#111111")


# =========================
# TITLE
# =========================

title_label = tk.Label(
    root,
    text="🤖 AbrarAI",
    font=("Arial", 24, "bold"),
    bg="#111111",
    fg="white"
)

title_label.pack(pady=(20, 5))


subtitle_label = tk.Label(
    root,
    text="Your Personal AI Assistant",
    font=("Arial", 11),
    bg="#111111",
    fg="#aaaaaa"
)

subtitle_label.pack(pady=(0, 15))


# =========================
# CHAT BOX
# =========================

chat_box = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Arial", 12),
    bg="#181818",
    fg="white",
    insertbackground="white",
    relief=tk.FLAT,
    padx=15,
    pady=15
)

chat_box.pack(
    fill=tk.BOTH,
    expand=True,
    padx=20,
    pady=10
)

chat_box.tag_config(
    "user",
    foreground="#4da6ff",
    font=("Arial", 12, "bold")
)

chat_box.tag_config(
    "ai",
    foreground="#00e676",
    font=("Arial", 12)
)

chat_box.config(state=tk.DISABLED)


# =========================
# WELCOME MESSAGE
# =========================

chat_box.config(state=tk.NORMAL)

chat_box.insert(
    tk.END,
    "AbrarAI: Hello sir! 👋\n"
    "AbrarAI is ready. Ask me anything.\n\n",
    "ai"
)

chat_box.config(state=tk.DISABLED)


# =========================
# INPUT FRAME
# =========================

input_frame = tk.Frame(
    root,
    bg="#111111"
)

input_frame.pack(
    fill=tk.X,
    padx=20,
    pady=(5, 10)
)


# =========================
# INPUT BOX
# =========================

user_input = tk.Entry(
    input_frame,
    font=("Arial", 13),
    bg="#222222",
    fg="white",
    insertbackground="white",
    relief=tk.FLAT
)

user_input.pack(
    side=tk.LEFT,
    fill=tk.X,
    expand=True,
    ipady=10,
    padx=(0, 10)
)


# Enter key
user_input.bind(
    "<Return>",
    send_message
)


# =========================
# SEND BUTTON
# =========================

send_button = tk.Button(
    input_frame,
    text="Send ➤",
    font=("Arial", 11, "bold"),
    bg="#333333",
    fg="white",
    relief=tk.FLAT,
    padx=18,
    pady=8,
    command=send_message
)

send_button.pack(side=tk.RIGHT)


# =========================
# BUTTON FRAME
# =========================

button_frame = tk.Frame(
    root,
    bg="#111111"
)

button_frame.pack(
    fill=tk.X,
    padx=20,
    pady=(0, 15)
)


# =========================
# NEW CHAT BUTTON
# =========================

new_chat_button = tk.Button(
    button_frame,
    text="➕ New Chat",
    font=("Arial", 10),
    bg="#333333",
    fg="white",
    relief=tk.FLAT,
    padx=12,
    pady=6,
    command=new_chat
)

new_chat_button.pack(
    side=tk.LEFT,
    padx=(0, 8)
)


# =========================
# CLEAR BUTTON
# =========================

clear_button = tk.Button(
    button_frame,
    text="🗑 Clear",
    font=("Arial", 10),
    bg="#333333",
    fg="white",
    relief=tk.FLAT,
    padx=12,
    pady=6,
    command=clear_chat
)

clear_button.pack(
    side=tk.LEFT,
    padx=8
)


# =========================
# THEME BUTTON
# =========================

theme_button = tk.Button(
    button_frame,
    text="☀️ Light Mode",
    font=("Arial", 10),
    bg="#333333",
    fg="white",
    relief=tk.FLAT,
    padx=12,
    pady=6,
    command=toggle_theme
)

theme_button.pack(
    side=tk.RIGHT
)


# =========================
# FOCUS INPUT
# =========================

user_input.focus_set()


# =========================
# START ABRARAI
# =========================

root.mainloop()
