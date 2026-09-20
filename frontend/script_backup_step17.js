// =====================================================
// INDUSTRIAL MAINTENANCE AI
// FRONTEND JAVASCRIPT
// =====================================================

const API_URL = "http://127.0.0.1:8000";

const TOKEN_KEY = "maintenance_ai_token";
const USERNAME_KEY = "maintenance_ai_username";
const HISTORY_KEY = "maintenance_ai_chat_history";
const ACTIVE_CHAT_KEY = "maintenance_ai_active_chat";

let currentMessages = [];
let chatHistory = [];
let currentChatId = null;


// =====================================================
// DOM ELEMENTS
// =====================================================

const authPage = document.getElementById("authPage");
const chatPage = document.getElementById("chatPage");

const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

const loginUsername = document.getElementById("loginUsername");
const loginPassword = document.getElementById("loginPassword");

const registerUsername =
    document.getElementById("registerUsername");

const registerEmail =
    document.getElementById("registerEmail");

const registerPassword =
    document.getElementById("registerPassword");

const loginError =
    document.getElementById("loginError");

const registerError =
    document.getElementById("registerError");

const registerSuccess =
    document.getElementById("registerSuccess");

const messagesContainer =
    document.getElementById("messages");

const messageInput =
    document.getElementById("messageInput");

const sendButton =
    document.getElementById("sendButton");

const chatHistoryContainer =
    document.getElementById("chatHistory");

const currentUsername =
    document.getElementById("currentUsername");

const languageIndicator =
    document.getElementById("languageIndicator");

const themeIcon =
    document.getElementById("themeIcon");

const themeText =
    document.getElementById("themeText");


// =====================================================
// PAGE INITIALIZATION
// =====================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadTheme();

        loadChatHistory();

        const token =
            localStorage.getItem(
                TOKEN_KEY
            );

        const username =
            localStorage.getItem(
                USERNAME_KEY
            );

        if (token && username) {

            showChatPage();

        } else {

            showAuthPage();
        }

        setupTextarea();
    }
);


// =====================================================
// AUTH PAGE
// =====================================================

function showAuthPage() {

    authPage.classList.remove(
        "hidden"
    );

    chatPage.classList.add(
        "hidden"
    );
}


// =====================================================
// CHAT PAGE
// =====================================================

function showChatPage() {

    authPage.classList.add(
        "hidden"
    );

    chatPage.classList.remove(
        "hidden"
    );

    updateUserInterface();

    loadActiveChat();

    renderChatHistory();
}


// =====================================================
// LOGIN / REGISTER UI
// =====================================================

function showRegister() {

    loginForm.classList.add(
        "hidden"
    );

    registerForm.classList.remove(
        "hidden"
    );

    clearAuthMessages();
}


function showLogin() {

    registerForm.classList.add(
        "hidden"
    );

    loginForm.classList.remove(
        "hidden"
    );

    clearAuthMessages();
}


function clearAuthMessages() {

    if (loginError) {
        loginError.textContent = "";
    }

    if (registerError) {
        registerError.textContent = "";
    }

    if (registerSuccess) {
        registerSuccess.textContent = "";
    }
}


// =====================================================
// REGISTER
// =====================================================

async function registerUser() {

    const username =
        registerUsername.value.trim();

    const email =
        registerEmail.value.trim();

    const password =
        registerPassword.value;

    clearAuthMessages();

    if (
        !username ||
        !email ||
        !password
    ) {

        registerError.textContent =
            "Please fill in all fields.";

        return;
    }

    if (password.length < 6) {

        registerError.textContent =
            "Password must contain at least 6 characters.";

        return;
    }

    try {

        const response =
            await fetch(
                `${API_URL}/register`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        username,
                        email,
                        password
                    })
                }
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Registration failed."
            );
        }

        registerSuccess.textContent =
            "Registration successful. You can now sign in.";

        registerUsername.value = "";
        registerEmail.value = "";
        registerPassword.value = "";

        setTimeout(
            () => {

                showLogin();

                loginUsername.value =
                    username;

            },
            1000
        );

    } catch (error) {

        registerError.textContent =
            error.message;
    }
}


// =====================================================
// LOGIN
// =====================================================

async function loginUser() {

    const username =
        loginUsername.value.trim();

    const password =
        loginPassword.value;

    clearAuthMessages();

    if (!username || !password) {

        loginError.textContent =
            "Please enter your username and password.";

        return;
    }

    try {

        const response =
            await fetch(
                `${API_URL}/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        username,
                        password
                    })
                }
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Login failed."
            );
        }

        localStorage.setItem(
            TOKEN_KEY,
            data.access_token
        );

        localStorage.setItem(
            USERNAME_KEY,
            data.username
        );

        currentChatId = null;
        currentMessages = [];

        localStorage.removeItem(
            ACTIVE_CHAT_KEY
        );

        showChatPage();

    } catch (error) {

        loginError.textContent =
            error.message;
    }
}


// =====================================================
// LOGOUT
// =====================================================

function logoutUser() {

    saveCurrentChat();

    localStorage.removeItem(
        TOKEN_KEY
    );

    localStorage.removeItem(
        USERNAME_KEY
    );

    localStorage.removeItem(
        ACTIVE_CHAT_KEY
    );

    currentChatId = null;
    currentMessages = [];

    showAuthPage();

    loginUsername.value = "";
    loginPassword.value = "";
}


// =====================================================
// USER INTERFACE
// =====================================================

function updateUserInterface() {

    const username =
        localStorage.getItem(
            USERNAME_KEY
        ) || "User";

    if (currentUsername) {

        currentUsername.textContent =
            username;
    }

    const avatar =
        document.querySelector(
            ".user-avatar"
        );

    if (avatar) {

        avatar.textContent =
            username
                .charAt(0)
                .toUpperCase();
    }
}


// =====================================================
// SEND MESSAGE
// =====================================================

async function sendMessage(
    customQuestion = null
) {

    const question =
        customQuestion !== null
            ? customQuestion.trim()
            : messageInput.value.trim();

    if (!question) {
        return;
    }


    // ---------------------------------------------
    // CREATE CHAT IF NECESSARY
    // ---------------------------------------------

    if (!currentChatId) {

        createNewChat(false);
    }


    // ---------------------------------------------
    // REMOVE WELCOME SCREEN
    // ---------------------------------------------

    removeWelcomeMessage();


    // ---------------------------------------------
    // ADD USER MESSAGE
    // ---------------------------------------------

    addUserMessage(
        question
    );


    // ---------------------------------------------
    // CLEAR INPUT
    // ---------------------------------------------

    if (messageInput) {

        messageInput.value = "";

        autoResizeTextarea();
    }


    // ---------------------------------------------
    // UI STATE
    // ---------------------------------------------

    updateLanguageIndicator(
        "Detecting language..."
    );

    setSendButtonState(true);

    showTypingIndicator();


    try {

        const token =
            localStorage.getItem(
                TOKEN_KEY
            );


        const response =
            await fetch(
                `${API_URL}/chat`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",

                        ...(token
                            ? {
                                "Authorization":
                                    `Bearer ${token}`
                            }
                            : {})
                    },

                    body: JSON.stringify({
                        question,
                        top_k: 5
                    })
                }
            );


        const data =
            await response.json();


        removeTypingIndicator();


        // -----------------------------------------
        // HANDLE AUTH ERROR
        // -----------------------------------------

        if (
            response.status === 401
        ) {

            localStorage.removeItem(
                TOKEN_KEY
            );

            alert(
                "Your session has expired. Please sign in again."
            );

            showAuthPage();

            return;
        }


        // -----------------------------------------
        // HANDLE OTHER ERRORS
        // -----------------------------------------

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to process the question."
            );
        }


        // -----------------------------------------
        // ADD AI RESPONSE
        // -----------------------------------------

        addAIMessage(
            data.answer,
            data.language,
            data.keywords || []
        );


        // -----------------------------------------
        // LANGUAGE
        // -----------------------------------------

        updateLanguageIndicator(
            getLanguageName(
                data.language
            )
        );


        // -----------------------------------------
        // SAVE CHAT
        // -----------------------------------------

        saveCurrentChat();


    } catch (error) {

        removeTypingIndicator();

        addAIMessage(
            "Sorry, an error occurred while communicating with the assistant.",
            "en",
            []
        );

        updateLanguageIndicator(
            "Connection error"
        );

        console.error(error);

    } finally {

        setSendButtonState(
            false
        );
    }
}


// =====================================================
// ADD USER MESSAGE
// =====================================================

function addUserMessage(text) {

    const message = {

        id: Date.now(),

        role: "user",

        content: text
    };

    currentMessages.push(
        message
    );

    renderMessage(
        message
    );

    scrollToBottom();
}


// =====================================================
// ADD AI MESSAGE
// =====================================================

function addAIMessage(
    text,
    language = "en",
    keywords = []
) {

    const message = {

        id: Date.now(),

        role: "assistant",

        content: text,

        language,

        keywords
    };

    currentMessages.push(
        message
    );

    renderMessage(
        message
    );

    scrollToBottom();
}


// =====================================================
// RENDER MESSAGE
// =====================================================

function renderMessage(
    message
) {

    const row =
        document.createElement(
            "div"
        );

    row.className =
        `message-row ${message.role}`;


    const bubble =
        document.createElement(
            "div"
        );

    bubble.className =
        "message-bubble";


    // =================================================
    // USER MESSAGE
    // =================================================

    if (
        message.role === "user"
    ) {

        bubble.textContent =
            message.content;


        const actions =
            document.createElement(
                "div"
            );

        actions.className =
            "message-actions";


        const editButton =
            document.createElement(
                "button"
            );

        editButton.textContent =
            "✏️ Edit";

        editButton.className =
            "message-action-button";


        editButton.onclick =
            () => {

                editUserMessage(
                    message
                );
            };


        actions.appendChild(
            editButton
        );


        row.appendChild(
            bubble
        );

        row.appendChild(
            actions
        );


    // =================================================
    // AI MESSAGE
    // =================================================

    } else {

        bubble.textContent =
            message.content;

        row.appendChild(
            bubble
        );


        // ---------------------------------------------
        // KEYWORDS
        // ---------------------------------------------

        if (
            message.keywords &&
            message.keywords.length > 0
        ) {

            const keywordContainer =
                document.createElement(
                    "div"
                );

            keywordContainer.className =
                "keyword-container";


            const keywordTitle =
                document.createElement(
                    "span"
                );

            keywordTitle.className =
                "keyword-title";

            keywordTitle.textContent =
                "Keywords:";


            keywordContainer.appendChild(
                keywordTitle
            );


            message.keywords.forEach(
                keyword => {

                    const chip =
                        document.createElement(
                            "span"
                        );

                    chip.className =
                        "keyword-chip";

                    chip.textContent =
                        keyword;

                    keywordContainer.appendChild(
                        chip
                    );
                }
            );


            row.appendChild(
                keywordContainer
            );
        }


        // Knowledge Sources intentionally hidden.
    }


    messagesContainer.appendChild(
        row
    );
}


// =====================================================
// RENDER CURRENT CHAT
// =====================================================

function renderCurrentMessages() {

    messagesContainer.innerHTML = "";

    if (
        currentMessages.length === 0
    ) {

        showWelcomeMessage();

        return;
    }


    currentMessages.forEach(
        message => {

            renderMessage(
                message
            );
        }
    );

    scrollToBottom();
}


// =====================================================
// EDIT USER MESSAGE
// =====================================================

function editUserMessage(
    message
) {

    const newText =
        prompt(
            "Edit your message:",
            message.content
        );


    if (
        newText === null ||
        newText.trim() === ""
    ) {

        return;
    }


    const editedText =
        newText.trim();


    const messageIndex =
        currentMessages.findIndex(
            item =>
                item.id === message.id
        );


    if (
        messageIndex === -1
    ) {

        return;
    }


    // ---------------------------------------------
    // REMOVE THE OLD MESSAGE AND EVERYTHING AFTER IT
    // ---------------------------------------------

    currentMessages =
        currentMessages.slice(
            0,
            messageIndex
        );


    renderCurrentMessages();


    // ---------------------------------------------
    // SEND EDITED MESSAGE AS NEW MESSAGE
    // ---------------------------------------------

    sendMessage(
        editedText
    );
}


// =====================================================
// TYPING INDICATOR
// =====================================================

function showTypingIndicator() {

    removeTypingIndicator();


    const row =
        document.createElement(
            "div"
        );

    row.className =
        "message-row assistant";

    row.id =
        "typingIndicator";


    const bubble =
        document.createElement(
            "div"
        );

    bubble.className =
        "message-bubble typing";


    bubble.innerHTML =
        `
        <span></span>
        <span></span>
        <span></span>
        `;


    row.appendChild(
        bubble
    );

    messagesContainer.appendChild(
        row
    );

    scrollToBottom();
}


function removeTypingIndicator() {

    const indicator =
        document.getElementById(
            "typingIndicator"
        );

    if (indicator) {

        indicator.remove();
    }
}


// =====================================================
// SEND BUTTON
// =====================================================

function setSendButtonState(
    disabled
) {

    if (!sendButton) {
        return;
    }

    sendButton.disabled =
        disabled;


    if (disabled) {

        sendButton.style.opacity =
            "0.6";

        sendButton.style.cursor =
            "not-allowed";

    } else {

        sendButton.style.opacity =
            "1";

        sendButton.style.cursor =
            "pointer";
    }
}


// =====================================================
// WELCOME SCREEN
// =====================================================

function showWelcomeMessage() {

    if (
        document.querySelector(
            ".welcome-message"
        )
    ) {

        return;
    }


    messagesContainer.innerHTML =
        `
        <div class="welcome-message">

            <div class="welcome-icon">
                ⚙
            </div>

            <h1>
                How can I help with
                industrial maintenance?
            </h1>

            <p>
                Ask questions about bearings,
                motors, pumps, lubrication,
                hydraulics and machine safety.
            </p>

            <div class="suggestions">

                <button
                    onclick="useSuggestion(
                        'What are the common causes of bearing failure?'
                    )"
                >
                    Bearing failure causes
                </button>

                <button
                    onclick="useSuggestion(
                        'What are common motor maintenance procedures?'
                    )"
                >
                    Motor maintenance
                </button>

                <button
                    onclick="useSuggestion(
                        'What causes hydraulic system contamination?'
                    )"
                >
                    Hydraulic contamination
                </button>

            </div>

        </div>
        `;
}


function removeWelcomeMessage() {

    const welcome =
        document.querySelector(
            ".welcome-message"
        );

    if (welcome) {

        welcome.remove();
    }
}


// =====================================================
// SUGGESTIONS
// =====================================================

function useSuggestion(
    question
) {

    messageInput.value =
        question;

    autoResizeTextarea();

    sendMessage();
}


// =====================================================
// CREATE NEW CHAT
// =====================================================

function createNewChat(
    savePrevious = true
) {

    if (
        savePrevious &&
        currentMessages.length > 0
    ) {

        saveCurrentChat();
    }


    // ---------------------------------------------
    // CREATE UNIQUE CHAT ID
    // ---------------------------------------------

    currentChatId =
        `chat_${Date.now()}_${Math.random()
            .toString(36)
            .substring(2, 8)}`;


    currentMessages = [];


    localStorage.setItem(
        ACTIVE_CHAT_KEY,
        currentChatId
    );


    messagesContainer.innerHTML =
        "";

    showWelcomeMessage();


    if (messageInput) {

        messageInput.value = "";

        autoResizeTextarea();
    }


    updateLanguageIndicator(
        "Auto language detection"
    );


    renderChatHistory();
}


// =====================================================
// NEW CHAT BUTTON
// =====================================================

function newChat() {

    createNewChat(
        true
    );
}


// =====================================================
// SAVE CURRENT CHAT
// =====================================================

function saveCurrentChat() {

    const username =
        localStorage.getItem(
            USERNAME_KEY
        );


    if (
        !username ||
        !currentChatId ||
        currentMessages.length === 0
    ) {

        return;
    }


    const firstUserMessage =
        currentMessages.find(
            message =>
                message.role === "user"
        );


    const title =
        firstUserMessage
            ? firstUserMessage.content
            : "New Chat";


    const chatIndex =
        chatHistory.findIndex(
            chat =>
                chat.id === currentChatId &&
                chat.username === username
        );


    const chatObject = {

        id: currentChatId,

        username,

        title,

        messages:
            JSON.parse(
                JSON.stringify(
                    currentMessages
                )
            ),

        updatedAt:
            new Date().toISOString()
    };


    if (
        chatIndex >= 0
    ) {

        chatHistory[
            chatIndex
        ] = chatObject;

    } else {

        chatHistory.unshift(
            chatObject
        );
    }


    saveChatHistory();

    renderChatHistory();
}


// =====================================================
// SAVE CHAT HISTORY
// =====================================================

function saveChatHistory() {

    localStorage.setItem(
        HISTORY_KEY,
        JSON.stringify(
            chatHistory
        )
    );
}


// =====================================================
// LOAD CHAT HISTORY
// =====================================================

function loadChatHistory() {

    const stored =
        localStorage.getItem(
            HISTORY_KEY
        );


    if (!stored) {

        chatHistory = [];

        return;
    }


    try {

        chatHistory =
            JSON.parse(
                stored
            );


        if (
            !Array.isArray(
                chatHistory
            )
        ) {

            chatHistory = [];
        }

    } catch (error) {

        console.error(
            "Unable to load chat history:",
            error
        );

        chatHistory = [];
    }
}


// =====================================================
// LOAD ACTIVE CHAT
// =====================================================

function loadActiveChat() {

    const username =
        localStorage.getItem(
            USERNAME_KEY
        );


    if (!username) {
        return;
    }


    const savedActiveChat =
        localStorage.getItem(
            ACTIVE_CHAT_KEY
        );


    if (savedActiveChat) {

        const chat =
            chatHistory.find(
                item =>
                    item.id ===
                        savedActiveChat &&
                    item.username ===
                        username
            );


        if (chat) {

            currentChatId =
                chat.id;

            currentMessages =
                JSON.parse(
                    JSON.stringify(
                        chat.messages || []
                    )
                );

            renderCurrentMessages();

            return;
        }
    }


    // ---------------------------------------------
    // IF THERE IS NO ACTIVE CHAT
    // ---------------------------------------------

    currentChatId = null;

    currentMessages = [];

    messagesContainer.innerHTML =
        "";

    showWelcomeMessage();
}


// =====================================================
// RENDER CHAT HISTORY
// =====================================================

function renderChatHistory() {

    if (!chatHistoryContainer) {
        return;
    }


    chatHistoryContainer.innerHTML =
        "";


    const username =
        localStorage.getItem(
            USERNAME_KEY
        );


    if (!username) {
        return;
    }


    const userChats =
        chatHistory
            .filter(
                chat =>
                    chat.username ===
                    username
            )
            .sort(
                (a, b) =>
                    new Date(
                        b.updatedAt
                    ) -
                    new Date(
                        a.updatedAt
                    )
            );


    if (
        userChats.length === 0
    ) {

        const empty =
            document.createElement(
                "p"
            );

        empty.className =
            "empty-history";

        empty.textContent =
            "No recent chats";

        chatHistoryContainer.appendChild(
            empty
        );

        return;
    }


    userChats.forEach(
        chat => {

            const item =
                document.createElement(
                    "div"
                );

            item.className =
                "history-item";


            const title =
                document.createElement(
                    "button"
                );

            title.className =
                "history-title";

            title.textContent =
                shortenText(
                    chat.title,
                    32
                );

            title.title =
                chat.title;


            // -----------------------------------------
            // ACTIVE CHAT
            // -----------------------------------------

            if (
                chat.id ===
                currentChatId
            ) {

                item.classList.add(
                    "active"
                );
            }


            title.onclick =
                () => {

                    loadChat(
                        chat.id
                    );
                };


            // -----------------------------------------
            // DELETE BUTTON
            // -----------------------------------------

            const deleteButton =
                document.createElement(
                    "button"
                );

            deleteButton.className =
                "history-delete";

            deleteButton.textContent =
                "×";

            deleteButton.title =
                "Delete this chat";


            deleteButton.onclick =
                event => {

                    event.stopPropagation();

                    deleteChat(
                        chat.id
                    );
                };


            item.appendChild(
                title
            );

            item.appendChild(
                deleteButton
            );


            chatHistoryContainer.appendChild(
                item
            );
        }
    );
}


// =====================================================
// LOAD SELECTED CHAT
// =====================================================

function loadChat(
    chatId
) {

    const username =
        localStorage.getItem(
            USERNAME_KEY
        );


    const chat =
        chatHistory.find(
            item =>
                item.id === chatId &&
                item.username ===
                    username
        );


    if (!chat) {
        return;
    }


    // ---------------------------------------------
    // SAVE CURRENT CHAT FIRST
    // ---------------------------------------------

    if (
        currentMessages.length > 0 &&
        currentChatId !== chatId
    ) {

        saveCurrentChat();
    }


    // ---------------------------------------------
    // LOAD SELECTED CHAT
    // ---------------------------------------------

    currentChatId =
        chat.id;


    currentMessages =
        JSON.parse(
            JSON.stringify(
                chat.messages || []
            )
        );


    localStorage.setItem(
        ACTIVE_CHAT_KEY,
        currentChatId
    );


    renderCurrentMessages();

    renderChatHistory();
}


// =====================================================
// DELETE ONE CHAT
// =====================================================

function deleteChat(
    chatId
) {

    const username =
        localStorage.getItem(
            USERNAME_KEY
        );


    const chat =
        chatHistory.find(
            item =>
                item.id === chatId &&
                item.username ===
                    username
        );


    if (!chat) {
        return;
    }


    const confirmed =
        confirm(
            "Delete this chat?"
        );


    if (!confirmed) {
        return;
    }


    // ---------------------------------------------
    // REMOVE ONLY SELECTED CHAT
    // ---------------------------------------------

    chatHistory =
        chatHistory.filter(
            item =>
                !(
                    item.id === chatId &&
                    item.username ===
                        username
                )
        );


    saveChatHistory();


    // ---------------------------------------------
    // IF CURRENT CHAT WAS DELETED
    // ---------------------------------------------

    if (
        currentChatId === chatId
    ) {

        currentChatId = null;

        currentMessages = [];


        localStorage.removeItem(
            ACTIVE_CHAT_KEY
        );


        messagesContainer.innerHTML =
            "";

        showWelcomeMessage();


        updateLanguageIndicator(
            "Auto language detection"
        );
    }


    renderChatHistory();
}


// =====================================================
// SHORTEN CHAT TITLE
// =====================================================

function shortenText(
    text,
    maxLength
) {

    if (!text) {

        return "New Chat";
    }


    if (
        text.length <= maxLength
    ) {

        return text;
    }


    return (
        text.substring(
            0,
            maxLength
        ) + "..."
    );
}


// =====================================================
// LANGUAGE
// =====================================================

function getLanguageName(
    language
) {

    const languages = {

        en: "English",

        sw: "Kiswahili",

        fr: "French"
    };


    return (
        languages[language] ||
        "English"
    );
}


function updateLanguageIndicator(
    text
) {

    if (languageIndicator) {

        languageIndicator.textContent =
            text;
    }
}


// =====================================================
// KEYBOARD
// =====================================================

function handleInputKey(
    event
) {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        sendMessage();
    }
}


// =====================================================
// TEXTAREA
// =====================================================

function setupTextarea() {

    if (!messageInput) {
        return;
    }


    messageInput.addEventListener(
        "input",
        autoResizeTextarea
    );
}


function autoResizeTextarea() {

    if (!messageInput) {
        return;
    }


    messageInput.style.height =
        "auto";


    messageInput.style.height =
        Math.min(
            messageInput.scrollHeight,
            150
        ) + "px";
}


// =====================================================
// SCROLL
// =====================================================

function scrollToBottom() {

    if (!messagesContainer) {
        return;
    }


    setTimeout(
        () => {

            messagesContainer.scrollTop =
                messagesContainer.scrollHeight;

        },
        50
    );
}


// =====================================================
// THEME
// =====================================================

function toggleTheme() {

    const currentTheme =
        document.body.classList.contains(
            "dark-mode"
        )
            ? "dark"
            : "light";


    const newTheme =
        currentTheme === "dark"
            ? "light"
            : "dark";


    applyTheme(
        newTheme
    );


    localStorage.setItem(
        "maintenance_ai_theme",
        newTheme
    );
}


function loadTheme() {

    const savedTheme =
        localStorage.getItem(
            "maintenance_ai_theme"
        );


    if (savedTheme) {

        applyTheme(
            savedTheme
        );

        return;
    }


    const prefersDark =
        window.matchMedia &&
        window.matchMedia(
            "(prefers-color-scheme: dark)"
        ).matches;


    applyTheme(
        prefersDark
            ? "dark"
            : "light"
    );
}


function applyTheme(
    theme
) {

    if (
        theme === "dark"
    ) {

        document.body.classList.add(
            "dark-mode"
        );


        if (themeIcon) {

            themeIcon.textContent =
                "☀️";
        }


        if (themeText) {

            themeText.textContent =
                "Light mode";
        }

    } else {

        document.body.classList.remove(
            "dark-mode"
        );


        if (themeIcon) {

            themeIcon.textContent =
                "🌙";
        }


        if (themeText) {

            themeText.textContent =
                "Dark mode";
        }
    }
}


// =====================================================
// ESCAPE HTML
// =====================================================

function escapeHTML(
    text
) {

    const div =
        document.createElement(
            "div"
        );

    div.textContent =
        text;

    return div.innerHTML;
}