
from flask import Flask, render_template_string, request, jsonify
from ai_brain import ask_ai
import urllib.parse

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AbrarAI</title>

<style>
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
}

body {
    font-family: Arial, Helvetica, sans-serif;
    background: #020617;
    color: white;
    overflow: hidden;
}

.background {
    position: fixed;
    inset: 0;
    overflow: hidden;
    z-index: 0;
}

.grid {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(59,130,246,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(59,130,246,0.05) 1px, transparent 1px);
    background-size: 55px 55px;
}

.glow {
    position: absolute;
    border-radius: 50%;
    filter: blur(100px);
    opacity: 0.28;
}

.glow1 {
    width: 400px;
    height: 400px;
    background: #2563eb;
    top: -180px;
    left: -120px;
}

.glow2 {
    width: 400px;
    height: 400px;
    background: #7c3aed;
    right: -160px;
    top: 25%;
}

.glow3 {
    width: 350px;
    height: 350px;
    background: #0891b2;
    bottom: -180px;
    left: 35%;
}

.app {
    position: relative;
    z-index: 2;
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
}

.header {
    height: 76px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 28px;
    background: rgba(2,6,23,0.78);
    border-bottom: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
}

.brand {
    display: flex;
    align-items: center;
    gap: 13px;
}

.logo {
    position: relative;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 15px;
    background: linear-gradient(135deg, #06b6d4, #2563eb 50%, #7c3aed);
    box-shadow:
        0 0 20px rgba(14,165,233,0.6),
        0 0 45px rgba(124,58,237,0.35);
    overflow: hidden;
    animation: logoPulse 3s infinite ease-in-out;
}

.logo::before {
    content: "";
    position: absolute;
    width: 27px;
    height: 27px;
    border: 2px solid white;
    border-radius: 7px;
    transform: rotate(45deg);
    box-shadow: 0 0 12px rgba(255,255,255,0.5);
}

.logo::after {
    content: "A";
    position: absolute;
    color: white;
    font-size: 20px;
    font-weight: 900;
    text-shadow: 0 0 8px white;
}

@keyframes logoPulse {
    0%, 100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.06);
    }
}

.brand-name {
    font-size: 23px;
    font-weight: 900;
    background: linear-gradient(90deg, white, #60a5fa, #a78bfa, #22d3ee);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.brand-subtitle {
    margin-top: 3px;
    color: #64748b;
    font-size: 9px;
    letter-spacing: 1.6px;
}

.status {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border-radius: 25px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    color: #86efac;
    font-size: 12px;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 12px #22c55e;
}

.chat {
    flex: 1;
    overflow-y: auto;
    padding: 20px 15px 30px;
}

.chat-container {
    width: 100%;
    max-width: 900px;
    margin: auto;
}

.welcome {
    min-height: 62vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.big-logo {
    position: relative;
    width: 112px;
    height: 112px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 34px;
    background: linear-gradient(135deg, #06b6d4, #2563eb 50%, #7c3aed);
    box-shadow:
        0 0 40px rgba(14,165,233,0.65),
        0 0 90px rgba(124,58,237,0.35);
    animation: floatLogo 4s infinite ease-in-out;
}

.big-logo::before {
    content: "";
    position: absolute;
    width: 58px;
    height: 58px;
    border: 4px solid white;
    border-radius: 14px;
    transform: rotate(45deg);
    box-shadow: 0 0 20px rgba(255,255,255,0.5);
}

.big-logo::after {
    content: "A";
    position: absolute;
    color: white;
    font-size: 43px;
    font-weight: 900;
    text-shadow: 0 0 12px white;
}

@keyframes floatLogo {
    0%, 100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-11px);
    }
}

.welcome h1 {
    margin: 29px 0 8px;
    font-size: 43px;
    letter-spacing: -1px;
    background: linear-gradient(90deg, white, #60a5fa, #a78bfa, #22d3ee, white);
    background-size: 250% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: shine 5s linear infinite;
}

@keyframes shine {
    to {
        background-position: 250% center;
    }
}

.welcome p {
    margin: 0;
    color: #94a3b8;
    font-size: 15px;
}

.quick {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
    margin-top: 28px;
}

.quick button {
    padding: 11px 16px;
    border-radius: 25px;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.04);
    color: #cbd5e1;
    cursor: pointer;
    transition: 0.25s;
}

.quick button:hover {
    transform: translateY(-3px);
    background: rgba(59,130,246,0.15);
    border-color: rgba(96,165,250,0.55);
}

.message-row {
    display: flex;
    margin-bottom: 22px;
}

.message-row.user {
    justify-content: flex-end;
}

.message {
    max-width: 78%;
    padding: 14px 17px;
    border-radius: 19px;
    font-size: 15px;
    line-height: 1.6;
    white-space: pre-wrap;
    word-break: break-word;
}

.message.user {
    background: linear-gradient(135deg, #2563eb, #4f46e5);
}

.message.ai {
    color: #e2e8f0;
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.08);
}

.typing {
    display: flex;
    gap: 5px;
    padding: 15px 18px;
    border-radius: 18px;
    background: rgba(255,255,255,0.055);
}

.typing span {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #60a5fa;
    animation: typing 1s infinite;
}

.typing span:nth-child(2) {
    animation-delay: 0.15s;
}

.typing span:nth-child(3) {
    animation-delay: 0.3s;
}

@keyframes typing {
    0%, 100% {
        opacity: 0.3;
        transform: translateY(0);
    }

    50% {
        opacity: 1;
        transform: translateY(-5px);
    }
}

.input-wrapper {
    flex-shrink: 0;
    padding: 8px 18px 17px;
    background: linear-gradient(transparent, rgba(2,6,23,0.95));
}

.input-container {
    width: 100%;
    max-width: 900px;
    margin: auto;
    display: flex;
    align-items: center;
    padding: 7px;
    border-radius: 20px;
    background: rgba(15,23,42,0.85);
    border: 1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(20px);
}

input {
    flex: 1;
    min-width: 0;
    padding: 14px;
    border: none;
    outline: none;
    background: transparent;
    color: white;
    font-size: 15px;
}

input::placeholder {
    color: #64748b;
}

.send {
    width: 48px;
    height: 48px;
    border: none;
    border-radius: 15px;
    color: white;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    cursor: pointer;
    font-size: 18px;
}

.send:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.disclaimer {
    text-align: center;
    margin-top: 8px;
    color: #475569;
    font-size: 10px;
}

@media (max-width: 600px) {

    .header {
        height: 65px;
        padding: 0 14px;
    }

    .logo {
        width: 40px;
        height: 40px;
        border-radius: 12px;
    }

    .logo::before {
        width: 22px;
        height: 22px;
    }

    .logo::after {
        font-size: 16px;
    }

    .brand-name {
        font-size: 18px;
    }

    .brand-subtitle {
        font-size: 7px;
    }

    .status {
        font-size: 10px;
        padding: 7px 10px;
    }

    .big-logo {
        width: 84px;
        height: 84px;
        border-radius: 25px;
    }

    .big-logo::before {
        width: 42px;
        height: 42px;
        border-width: 3px;
    }

    .big-logo::after {
        font-size: 31px;
    }

    .welcome h1 {
        font-size: 30px;
    }

    .welcome p {
        font-size: 13px;
    }

    .quick {
        gap: 7px;
    }

    .quick button {
        padding: 8px 11px;
        font-size: 10px;
    }

    .message {
        max-width: 88%;
        font-size: 14px;
    }

    .input-wrapper {
        padding: 6px 10px 11px;
    }

    input {
        font-size: 14px;
        padding: 12px 9px;
    }

    .send {
        width: 43px;
        height: 43px;
    }
}

</style>
</head>

<body>

<div class="background">
    <div class="grid"></div>
    <div class="glow glow1"></div>
    <div class="glow glow2"></div>
    <div class="glow glow3"></div>
</div>

<div class="app">

<header class="header">

    <div class="brand">

        <div class="logo"></div>

        <div>
            <div class="brand-name">AbrarAI</div>
            <div class="brand-subtitle">PERSONAL AI ASSISTANT</div>
        </div>

    </div>

    <div class="status">
        <div class="status-dot"></div>
        Online
    </div>

</header>


<main class="chat" id="chat">

    <div class="chat-container" id="chatContainer">

        <div class="welcome" id="welcome">

            <div class="big-logo"></div>

            <h1>Welcome to AbrarAI</h1>

            <p>Your personal AI assistant</p>

            <div class="quick">

                <button onclick="quickMessage('What can you do?')">
                    ✨ What can you do?
                </button>

                <button onclick="quickMessage('Explain Python simply')">
                    🐍 Learn Python
                </button>

                <button onclick="quickMessage('What is HTML?')">
                    🌐 Explain HTML
                </button>

                <button onclick="quickMessage('Tell me a joke')">
                    😂 Tell me a joke
                </button>

            </div>

        </div>

    </div>

</main>


<div class="input-wrapper">

    <div class="input-container">

        <input
            id="message"
            type="text"
            placeholder="Message AbrarAI..."
            autocomplete="off"
        >

        <button
            class="send"
            id="sendButton"
            onclick="sendMessage()"
        >
            ➤
        </button>

    </div>

    <div class="disclaimer">
        AbrarAI may make mistakes. Check important information.
    </div>

</div>

</div>


<script>

function quickMessage(text) {

    const input = document.getElementById("message");

    input.value = text;

    sendMessage();
}


async function sendMessage() {

    const input = document.getElementById("message");

    const button = document.getElementById("sendButton");

    const chat = document.getElementById("chat");

    const container = document.getElementById("chatContainer");

    const message = input.value.trim();


    if (!message) {
        return;
    }


    const welcome = document.getElementById("welcome");

    if (welcome) {
        welcome.remove();
    }


    const userRow = document.createElement("div");

    userRow.className = "message-row user";


    const userBubble = document.createElement("div");

    userBubble.className = "message user";

    userBubble.innerText = message;


    userRow.appendChild(userBubble);

    container.appendChild(userRow);


    input.value = "";

    button.disabled = true;


    const typingRow = document.createElement("div");

    typingRow.className = "message-row ai";

    typingRow.id = "typingRow";


    const typing = document.createElement("div");

    typing.className = "typing";

    typing.innerHTML =
        "<span></span><span></span><span></span>";


    typingRow.appendChild(typing);

    container.appendChild(typingRow);


    chat.scrollTop = chat.scrollHeight;


    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });


        const data = await response.json();


        const currentTyping =
            document.getElementById("typingRow");


        if (currentTyping) {
            currentTyping.remove();
        }


        const aiRow =
            document.createElement("div");

        aiRow.className =
            "message-row ai";


        const aiBubble =
            document.createElement("div");

        aiBubble.className =
            "message ai";


        aiBubble.innerText =
            data.response ||
            "Sorry sir, I could not respond.";


        aiRow.appendChild(aiBubble);

        container.appendChild(aiRow);


        chat.scrollTop =
            chat.scrollHeight;


    } catch (error) {

        console.error(error);


        const currentTyping =
            document.getElementById("typingRow");


        if (currentTyping) {
            currentTyping.remove();
        }


        const errorRow =
            document.createElement("div");

        errorRow.className =
            "message-row ai";


        const errorBubble =
            document.createElement("div");

        errorBubble.className =
            "message ai";


        errorBubble.innerText =
            "Sorry sir, something went wrong. 😔";


        errorRow.appendChild(errorBubble);

        container.appendChild(errorRow);


        chat.scrollTop =
            chat.scrollHeight;
    }


    button.disabled = false;

    input.focus();
}


document
    .getElementById("message")
    .addEventListener("keydown", function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();
        }

    });

</script>

</body>
</html>
"""


def get_response(message):

    message = message.strip()

    if not message:
        return "Please type a message, sir."


    if message.lower().startswith("search "):

        query = message[7:].strip()

        if not query:
            return "Please tell me what you want to search for, sir. 🔎"

        search_url = (
            "https://www.google.com/search?q="
            + urllib.parse.quote_plus(query)
        )

        return (
            "Here is your Google search, sir. 🔎\n\n"
            + search_url
        )


    try:

        response = ask_ai(message)

        if response:
            return response

        return "I'm still learning, sir. 🧠"


    except Exception as error:

        print("AI ERROR:", error)

        return "Sorry sir, something went wrong. 😔"


@app.route("/")
def home():

    return render_template_string(HTML)


@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "response": "Please type a message, sir."
            })


        message = data.get("message", "").strip()

        if not message:

            return jsonify({
                "response": "Please type a message, sir."
            })


        response = get_response(message)

        return jsonify({
            "response": response
        })


    except Exception as error:

        print("SERVER ERROR:", error)

        return jsonify({
            "response": "Something went wrong, sir. 😔"
        })


if __name__ == "__main__":

    print("")
    print("======================================")
    print("              ABRARAI")
    print("       PREMIUM AI ASSISTANT")
    print("======================================")
    print("")
    print("Open in browser:")
    print("http://127.0.0.1:5000")
    print("")
    print("Press CTRL+C to stop.")
    print("")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
