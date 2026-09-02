
import json
import os
import datetime

MEMORY_FILE = "memory.json"


# ==========================================
# LOAD MEMORY
# ==========================================

def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return {}

    try:

        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except:

        return {}


# ==========================================
# SAVE MEMORY
# ==========================================

def save_memory(memory):

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4)


# ==========================================
# AI BRAIN
# ==========================================

def ask_ai(question):

    question = question.strip()
    lower = question.lower()

    memory = load_memory()


    # ======================================
    # HELLO
    # ======================================

    if lower in ["hello", "hi", "hey", "hii", "hello abrarai"]:

        return "Hello sir! 👋 How can I help you?"


    # ======================================
    # WHO ARE YOU
    # ======================================

    if "who are you" in lower or "your name" in lower:

        return "I am AbrarAI, your personal local AI assistant. 🤖"


    # ======================================
    # HOW ARE YOU
    # ======================================

    if "how are you" in lower:

        return "I'm doing great, sir! 🤖"


    # ======================================
    # THANK YOU
    # ======================================

    if "thank" in lower:

        return "You're welcome, sir! 😊"


    # ======================================
    # NAME MEMORY
    # ======================================

    if lower.startswith("my name is "):

        name = question[11:].strip()

        if name:

            memory["name"] = name

            save_memory(memory)

            return f"Okay sir! I'll remember your name is {name}. 🧠"


    if "what is my name" in lower:

        name = memory.get("name")

        if name:

            return f"Your name is {name}, sir. 😊"

        return "You haven't told me your name yet, sir."


    # ======================================
    # FAVORITE COLOR
    # ======================================

    if lower.startswith("my favorite color is "):

        color = question[21:].strip()

        if color:

            memory["favorite_color"] = color

            save_memory(memory)

            return f"Got it sir! I'll remember your favorite color is {color}. 🎨"


    if "what is my favorite color" in lower:

        color = memory.get("favorite_color")

        if color:

            return f"Your favorite color is {color}. 🎨"

        return "You haven't told me your favorite color yet."


    # ======================================
    # FAVORITE FOOD
    # ======================================

    if lower.startswith("my favorite food is "):

        food = question[20:].strip()

        if food:

            memory["favorite_food"] = food

            save_memory(memory)

            return f"Got it sir! I'll remember your favorite food is {food}. 🍽️"


    if "what is my favorite food" in lower:

        food = memory.get("favorite_food")

        if food:

            return f"Your favorite food is {food}. 🍽️"

        return "You haven't told me your favorite food yet."


    # ======================================
    # FAVORITE GAME
    # ======================================

    if lower.startswith("my favorite game is "):

        game = question[20:].strip()

        if game:

            memory["favorite_game"] = game

            save_memory(memory)

            return f"Got it sir! I'll remember your favorite game is {game}. 🎮"


    if "what is my favorite game" in lower:

        game = memory.get("favorite_game")

        if game:

            return f"Your favorite game is {game}. 🎮"

        return "You haven't told me your favorite game yet."


    # ======================================
    # STUDY
    # ======================================

    if lower.startswith("i study "):

        study = question[8:].strip()

        if study:

            memory["study"] = study

            save_memory(memory)

            return f"Okay sir! I'll remember that you study {study}. 📚"


    if "what do i study" in lower:

        study = memory.get("study")

        if study:

            return f"You study {study}, sir. 📚"

        return "You haven't told me what you study yet."


    # ======================================
    # LIKE / INTEREST
    # ======================================

    if lower.startswith("i like "):

        interest = question[7:].strip()

        if interest:

            interests = memory.get("likes", [])

            if interest not in interests:

                interests.append(interest)

            memory["likes"] = interests

            save_memory(memory)

            return f"Got it sir! I'll remember that you like {interest}. ❤️"


    # ======================================
    # SHOW MEMORY
    # ======================================

    if lower in [
        "show my memory",
        "show memory",
        "what do you remember",
        "what do you know about me"
    ]:

        if not memory:

            return "My memory is empty, sir. 🧠"

        result = "Here's what I remember about you, sir: 🧠\n\n"

        if "name" in memory:
            result += f"👤 Name: {memory['name']}\n"

        if "favorite_color" in memory:
            result += f"🎨 Favorite color: {memory['favorite_color']}\n"

        if "favorite_food" in memory:
            result += f"🍽️ Favorite food: {memory['favorite_food']}\n"

        if "favorite_game" in memory:
            result += f"🎮 Favorite game: {memory['favorite_game']}\n"

        if "study" in memory:
            result += f"📚 Study: {memory['study']}\n"

        if "likes" in memory:

            for item in memory["likes"]:
                result += f"❤️ Likes: {item}\n"

        return result


    # ======================================
    # CLEAR MEMORY
    # ======================================

    if lower in [
        "clear memory",
        "delete memory",
        "forget everything"
    ]:

        save_memory({})

        return "Okay sir! 🧠 I've cleared my local memory."


    # ======================================
    # TIME
    # ======================================

    if lower == "time" or "current time" in lower:

        current_time = datetime.datetime.now().strftime("%I:%M %p")

        return f"Sir, the current time is {current_time}. ⏰"


    # ======================================
    # DATE
    # ======================================

    if lower == "date" or "today" in lower:

        current_date = datetime.datetime.now().strftime("%d %B %Y")

        return f"Today is {current_date}. 📅"


    # ======================================
    # PYTHON
    # ======================================

    if "python" in lower:

        return (
            "Python is a programming language. 🐍\n\n"
            "It is used for AI, websites, automation, "
            "software and data science."
        )


    # ======================================
    # HTML
    # ======================================

    if "html" in lower:

        return (
            "HTML creates the structure of a website. 🌐\n\n"
            "It is used for headings, paragraphs, "
            "buttons, images and other web elements."
        )


    # ======================================
    # CSS
    # ======================================

    if "css" in lower:

        return (
            "CSS is used to style websites. 🎨\n\n"
            "It controls colors, fonts, spacing, "
            "layouts and animations."
        )


    # ======================================
    # JAVASCRIPT
    # ======================================

    if "javascript" in lower:

        return (
            "JavaScript makes websites interactive. ⚡\n\n"
            "It can handle buttons, forms, animations "
            "and dynamic content."
        )


    # ======================================
    # FALLBACK
    # ======================================

    return (
        "I'm AbrarAI, your local assistant. 🤖\n\n"
        "I currently work without an online API.\n"
        "You can teach me things using commands like:\n\n"
        "• My name is Abrar\n"
        "• My favorite color is blue\n"
        "• My favorite food is biryani\n"
        "• My favorite game is BGMI\n"
        "• I study B.Tech\n"
        "• I like coding\n"
        "• Show my memory"
    )

