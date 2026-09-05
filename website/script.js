// ==========================================
// ABRARAI WEBSITE
// ==========================================

// =========================
// ELEMENTS
// =========================

const chatArea = document.getElementById("chatArea");
const messageInput = document.getElementById("messageInput");
const loginModal = document.getElementById("loginModal");
const chatHistory = document.getElementById("chatHistory");

let authMode = "login";

let chats = JSON.parse(
    localStorage.getItem("abrarAIChats") || "[]"
);

let currentChatId =
    localStorage.getItem("abrarAICurrentChat");


// =========================
// CHAT SYSTEM
// =========================

function createChat() {

    const chat = {
        id: Date.now().toString(),
        title: "New Chat",
        messages: []
    };

    chats.unshift(chat);

    currentChatId = chat.id;

    saveChats();
    renderChatList();
    renderCurrentChat();

    messageInput.focus();
}


// =========================
// GET CURRENT CHAT
// =========================

function getCurrentChat() {

    return chats.find(
        chat => chat.id === currentChatId
    );
}


// =========================
// SAVE CHATS
// =========================

function saveChats() {

    localStorage.setItem(
        "abrarAIChats",
        JSON.stringify(chats)
    );

    localStorage.setItem(
        "abrarAICurrentChat",
        currentChatId || ""
    );
}


// =========================
// RENDER CHAT LIST
// =========================

function renderChatList() {

    chatHistory.innerHTML = "";

    if (chats.length === 0) {

        const empty = document.createElement("div");

        empty.className = "chat-item";

        empty.textContent = "No chats yet";

        chatHistory.appendChild(empty);

        return;
    }

    chats.forEach(function(chat) {

        const item =
            document.createElement("div");

        item.className = "chat-item";

        if (chat.id === currentChatId) {
            item.classList.add("active");
        }

        item.textContent =
            chat.title || "New Chat";

        item.title =
            chat.title || "New Chat";

        item.onclick = function() {

            openChat(chat.id);

        };

        chatHistory.appendChild(item);

    });
}


// =========================
// OPEN CHAT
// =========================

function openChat(chatId) {

    const chat =
        chats.find(
            chat => chat.id === chatId
        );

    if (!chat) {
        return;
    }

    currentChatId = chatId;

    saveChats();

    renderChatList();

    renderCurrentChat();

    messageInput.focus();
}


// =========================
// RENDER CURRENT CHAT
// =========================

function renderCurrentChat() {

    chatArea.innerHTML = "";

    const chat =
        getCurrentChat();

    if (!chat || chat.messages.length === 0) {

        chatArea.innerHTML = `
            <div class="welcome">

                <div class="welcome-icon">
                    🤖
                </div>

                <h1>
                    Hello, Abrar 👋
                </h1>

                <p>
                    I'm AbrarAI, your personal AI assistant.
                </p>

                <p>
                    Ask me anything.
                </p>

            </div>
        `;

        return;
    }

    chat.messages.forEach(function(message) {

        addMessageToScreen(
            message.text,
            message.type
        );

    });

    chatArea.scrollTop =
        chatArea.scrollHeight;
}


// =========================
// ADD MESSAGE TO SCREEN
// =========================

function addMessageToScreen(text, type) {

    const div =
        document.createElement("div");

    div.className =
        "message " + type;

    div.textContent =
        text;

    chatArea.appendChild(div);

    return div;
}


// =========================
// ADD MESSAGE
// =========================

function addMessage(text, type) {

    const div =
        addMessageToScreen(text, type);

    const chat =
        getCurrentChat();

    if (!chat) {
        return div;
    }

    chat.messages.push({
        text: text,
        type: type
    });

    saveChats();

    chatArea.scrollTop =
        chatArea.scrollHeight;

    return div;
}


// =========================
// SEND MESSAGE
// =========================

async function sendMessage() {

    const message =
        messageInput.value.trim();

    if (message === "") {
        return;
    }


    // Agar koi chat nahi hai
    // to automatically new chat create karo

    if (!currentChatId) {

        createChat();

    }


    const chat =
        getCurrentChat();

    if (!chat) {
        return;
    }


    // Welcome remove

    const welcome =
        chatArea.querySelector(".welcome");

    if (welcome) {
        welcome.remove();
    }


    // User message

    addMessage(
        message,
        "user"
    );


    // First message ko chat title banao

    if (
        chat.title === "New Chat" ||
        chat.messages.length === 1
    ) {

        chat.title =
            createChatTitle(message);

        saveChats();

        renderChatList();

    }


    messageInput.value = "";


    // Thinking

    const thinking =
        addMessage(
            "Thinking... 🤔",
            "ai"
        );


    try {

        const response =
            await fetch(
                "/api/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );


        const data =
            await response.json();


        // Thinking remove

        if (thinking) {
            thinking.remove();
        }


        // Thinking ko saved chat se bhi remove

        const currentChat =
            getCurrentChat();

        if (currentChat) {

            currentChat.messages =
                currentChat.messages.filter(
                    item =>
                        !(
                            item.text ===
                            "Thinking... 🤔"
                            &&
                            item.type === "ai"
                        )
                );

        }


        if (
            response.ok &&
            data.response
        ) {

            addMessage(
                data.response,
                "ai"
            );

        } else {

            addMessage(
                data.response ||
                "Sorry sir, kuch problem aa gayi.",
                "ai"
            );

        }

    } catch (error) {

        console.error(
            "Chat error:",
            error
        );


        if (thinking) {
            thinking.remove();
        }


        const currentChat =
            getCurrentChat();

        if (currentChat) {

            currentChat.messages =
                currentChat.messages.filter(
                    item =>
                        !(
                            item.text ===
                            "Thinking... 🤔"
                            &&
                            item.type === "ai"
                        )
                );

            saveChats();

        }


        addMessage(
            "Python server se connection nahi ho raha. ⚠️",
            "ai"
        );

    }


    messageInput.focus();
}


// =========================
// CREATE CHAT TITLE
// =========================

function createChatTitle(message) {

    let title =
        message.trim();

    if (title.length > 28) {

        title =
            title.substring(0, 28) +
            "...";

    }

    return title;
}


// =========================
// NEW CHAT
// =========================

function newChat() {

    createChat();

}


// =========================
// ENTER KEY
// =========================

function handleEnter(event) {

    if (event.key === "Enter") {

        event.preventDefault();

        sendMessage();

    }
}


// =========================
// LOGIN MODAL
// =========================

function openLogin() {

    loginModal.style.display =
        "flex";

}


function closeLogin() {

    loginModal.style.display =
        "none";

}


// =========================
// LOGIN / SIGNUP SWITCH
// =========================

function switchAuthMode() {

    const title =
        document.getElementById(
            "authTitle"
        );

    const subtitle =
        document.getElementById(
            "authSubtitle"
        );

    const button =
        document.getElementById(
            "authButton"
        );

    const switchText =
        document.getElementById(
            "switchText"
        );

    const switchButton =
        document.getElementById(
            "switchButton"
        );


    if (authMode === "login") {

        authMode = "signup";

        title.textContent =
            "Create your AbrarAI account";

        subtitle.textContent =
            "Sign up to continue";

        button.textContent =
            "Sign Up";

        switchText.textContent =
            "Already have an account?";

        switchButton.textContent =
            "Login";

    } else {

        authMode = "login";

        title.textContent =
            "Welcome to AbrarAI";

        subtitle.textContent =
            "Login to continue";

        button.textContent =
            "Continue";

        switchText.textContent =
            "Don't have an account?";

        switchButton.textContent =
            "Sign Up";

    }

}


// =========================
// LOGIN / SIGNUP
// =========================

async function submitAuth() {

    const emailInput =
        document.getElementById(
            "emailInput"
        );

    const passwordInput =
        document.getElementById(
            "passwordInput"
        );


    const email =
        emailInput.value.trim();

    const password =
        passwordInput.value;


    if (
        email === "" ||
        password === ""
    ) {

        alert(
            "Email aur password enter karo."
        );

        return;
    }


    const url =
        authMode === "login"
            ? "/api/login"
            : "/api/signup";


    try {

        const response =
            await fetch(
                url,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                }
            );


        const data =
            await response.json();


        if (
            !response.ok ||
            !data.success
        ) {

            alert(
                data.message ||
                "Something went wrong."
            );

            return;
        }


        if (
            authMode === "signup"
        ) {

            alert(
                "Account create ho gaya! 🎉"
            );


            const loginResponse =
                await fetch(
                    "/api/login",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            email: email,
                            password: password
                        })
                    }
                );


            const loginData =
                await loginResponse.json();


            if (
                loginResponse.ok &&
                loginData.success
            ) {

                updateProfile(email);

                closeLogin();

            } else {

                alert(
                    "Account ban gaya. Ab Login karo."
                );

                authMode = "login";

                switchAuthMode();

            }

        } else {

            alert(
                "Login successful! Welcome to AbrarAI 🤖"
            );

            updateProfile(email);

            closeLogin();

        }


        emailInput.value = "";

        passwordInput.value = "";


    } catch (error) {

        console.error(
            "Auth error:",
            error
        );

        alert(
            "Server se connection nahi ho raha."
        );

    }

}


// =========================
// PROFILE
// =========================

function updateProfile(email) {

    const profileButton =
        document.getElementById(
            "profileButton"
        );


    if (!profileButton) {
        return;
    }


    const username =
        email.split("@")[0];


    profileButton.textContent =
        "👤 " + username;


    profileButton.onclick =
        function() {

            const logout =
                confirm(
                    "Logged in as:\n" +
                    email +
                    "\n\nOK = Logout\nCancel = Stay logged in"
                );


            if (logout) {

                logoutUser();

            }

        };

}


// =========================
// LOGOUT
// =========================

async function logoutUser() {

    try {

        const response =
            await fetch(
                "/api/logout",
                {
                    method: "POST"
                }
            );


        const data =
            await response.json();


        if (data.success) {

            alert(
                "Logout successful 👋"
            );


            const profileButton =
                document.getElementById(
                    "profileButton"
                );


            profileButton.textContent =
                "Login";


            profileButton.onclick =
                openLogin;

        }

    } catch (error) {

        console.error(
            "Logout error:",
            error
        );

        alert(
            "Logout nahi ho paya."
        );

    }

}


// =========================
// GOOGLE LOGIN
// =========================

function googleLogin() {

    alert(
        "Google Login abhi setup nahi hua hai."
    );

}


// =========================
// PHONE LOGIN
// =========================

function phoneLogin() {

    alert(
        "Phone OTP Login abhi setup nahi hua hai."
    );

}


// =========================
// DARK / LIGHT MODE
// =========================

function toggleTheme() {

    document.body.classList.toggle(
        "light-mode"
    );


    const light =
        document.body.classList.contains(
            "light-mode"
        );


    localStorage.setItem(
        "abrarAITheme",
        light
            ? "light"
            : "dark"
    );

}


if (
    localStorage.getItem(
        "abrarAITheme"
    ) === "light"
) {

    document.body.classList.add(
        "light-mode"
    );

}


// =========================
// CLOSE MODAL OUTSIDE
// =========================

loginModal.addEventListener(
    "click",
    function(event) {

        if (
            event.target ===
            loginModal
        ) {

            closeLogin();

        }

    }
);


// =========================
// HTML FUNCTIONS
// =========================

window.sendMessage =
    sendMessage;

window.handleEnter =
    handleEnter;

window.newChat =
    newChat;

window.openChat =
    openChat;

window.openLogin =
    openLogin;

window.closeLogin =
    closeLogin;

window.switchAuthMode =
    switchAuthMode;

window.submitAuth =
    submitAuth;

window.googleLogin =
    googleLogin;

window.phoneLogin =
    phoneLogin;

window.toggleTheme =
    toggleTheme;

window.logoutUser =
    logoutUser;


// =========================
// START ABRARAI
// =========================

// Agar purani chats nahi hain
// to ek new chat automatically banao

if (chats.length === 0) {

    createChat();

} else {

    // Agar saved current chat milti hai
    // to wahi open karo

    const exists =
        chats.some(
            chat =>
                chat.id === currentChatId
        );


    if (!exists) {

        currentChatId =
            chats[0].id;

    }

    saveChats();

    renderChatList();

    renderCurrentChat();

}


// Login check

async function checkLogin() {

    try {

        const response =
            await fetch("/api/me");

        const data =
            await response.json();


        if (data.logged_in) {

            updateProfile(
                data.email
            );

        }

    } catch (error) {

        console.error(
            "Login check error:",
            error
        );

    }

}


checkLogin();


// Input focus

messageInput.focus();