// ============================================
// CONFIGURATION
// ============================================

const API_URL = "http://localhost:8000";


// ============================================
// USER ID
// ============================================

let userId = localStorage.getItem(
    "college_rag_user_id"
);

if (!userId) {

    userId = crypto.randomUUID();

    localStorage.setItem(
        "college_rag_user_id",
        userId
    );
}


// ============================================
// DOM ELEMENTS
// ============================================

const chatContainer =
    document.getElementById("chatContainer");

const chatForm =
    document.getElementById("chatForm");

const questionInput =
    document.getElementById("questionInput");

const sendBtn =
    document.getElementById("sendBtn");

const pdfInput =
    document.getElementById("pdfInput");

const selectedFile =
    document.getElementById("selectedFile");

const uploadBtn =
    document.getElementById("uploadBtn");

const uploadStatus =
    document.getElementById("uploadStatus");

const welcome =
    document.getElementById("welcome");


// ============================================
// PDF SELECTION
// ============================================

pdfInput.addEventListener(
    "change",
    function () {

        const file = this.files[0];

        if (!file) {

            selectedFile.classList.add("hidden");

            return;
        }

        selectedFile.classList.remove("hidden");

        selectedFile.innerHTML = `
            📄 ${escapeHTML(file.name)}
        `;
    }
);


// ============================================
// UPLOAD PDF
// ============================================

async function uploadPDF() {

    const file = pdfInput.files[0];

    if (!file) {

        uploadStatus.innerHTML =
            "Please select a PDF first.";

        return;
    }


    if (
        !file.name
            .toLowerCase()
            .endsWith(".pdf")
    ) {

        uploadStatus.innerHTML =
            "Only PDF files are supported.";

        return;
    }


    uploadBtn.disabled = true;

    uploadBtn.innerText =
        "Uploading...";


    uploadStatus.innerHTML =
        "Processing document...";


    try {

        const formData =
            new FormData();

        formData.append(
            "file",
            file
        );

        formData.append(
            "user_id",
            userId
        );


        const response =
            await fetch(
                `${API_URL}/documents/upload`,
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Upload failed"
            );
        }


        uploadStatus.innerHTML = `
            <span style="color:#16a34a">
                ✓ Uploaded successfully
            </span>
            <br>
            ${data.chunks_created} chunks indexed.
        `;


        pdfInput.value = "";

        selectedFile.classList.add(
            "hidden"
        );


    } catch (error) {

        console.error(error);

        uploadStatus.innerHTML = `
            <span style="color:#dc2626">
                ✕ ${escapeHTML(error.message)}
            </span>
        `;

    } finally {

        uploadBtn.disabled = false;

        uploadBtn.innerText =
            "Upload Document";
    }
}


// ============================================
// CHAT FORM
// ============================================

chatForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const question =
            questionInput.value.trim();


        if (!question) {
            return;
        }


        await askQuestion(question);
    }
);


// ============================================
// ASK QUESTION
// ============================================

async function askQuestion(question) {

    // Remove welcome screen

    if (welcome) {
        welcome.remove();
    }


    // Display user message

    addMessage(
        "user",
        question
    );


    // Clear input

    questionInput.value = "";

    autoResize();


    // Disable input

    setLoading(true);


    // Loading message

    const loadingId =
        addLoadingMessage();


    try {

        const response =
            await fetch(
                `${API_URL}/chat`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question: question,
                        user_id: userId
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Failed to get answer"
            );
        }


        // Remove loading

        removeLoadingMessage(
            loadingId
        );


        // Display answer

        addAssistantMessage(
            data.answer,
            data.citations,
            data.route
        );


    } catch (error) {

        console.error(error);


        removeLoadingMessage(
            loadingId
        );


        addAssistantMessage(
            `Sorry, something went wrong.

${error.message}

Please make sure the FastAPI backend is running.`,
            [],
            null
        );


    } finally {

        setLoading(false);
    }
}


// ============================================
// ADD USER MESSAGE
// ============================================

function addMessage(
    role,
    text
) {

    const message =
        document.createElement("div");


    message.className =
        `message ${role}`;


    if (role === "user") {

        message.innerHTML = `

            <div class="message-content">

                <div class="message-role">
                    YOU
                </div>

                <div class="message-bubble">
                    ${escapeHTML(text)}
                </div>

            </div>

        `;

    }


    chatContainer.appendChild(
        message
    );


    scrollToBottom();
}


// ============================================
// ADD ASSISTANT MESSAGE
// ============================================

function addAssistantMessage(
    answer,
    citations = [],
    route = null
) {

    const message =
        document.createElement("div");


    message.className =
        "message assistant";


    let sourcesHTML = "";


    if (
        citations &&
        citations.length > 0
    ) {

        sourcesHTML = `

            <div class="sources">

                <div class="sources-title">
                    SOURCES
                </div>

                ${citations
                    .map(
                        createSourceHTML
                    )
                    .join("")
                }

            </div>
        `;
    }


    let routeHTML = "";


    if (route) {

        let routeName =
            route === "hybrid"
                ? "College + Web"
                : "College Documents";


        routeHTML = `
            <div class="route-badge">
                ${routeName}
            </div>
        `;
    }


    message.innerHTML = `

        <div class="message-avatar">
            🎓
        </div>


        <div class="message-content">

            <div class="message-role">
                COLLEGE AI
            </div>

            <div class="message-bubble">
                ${formatAnswer(answer)}
            </div>

            ${routeHTML}

            ${sourcesHTML}

        </div>

    `;


    chatContainer.appendChild(
        message
    );


    scrollToBottom();
}


// ============================================
// CREATE SOURCE
// ============================================

function createSourceHTML(
    citation
) {

    const name =
        citation.document_name ||
        "Unknown source";


    const page =
        citation.page_number
            ? `Page ${citation.page_number}`
            : "";


    const sourceType =
        citation.source_type ||
        "document";


    let link = "";


    if (citation.url) {

        link = `
            <a
                href="${escapeAttribute(
                    citation.url
                )}"
                target="_blank"
                rel="noopener noreferrer"
            >
                Open
            </a>
        `;
    }


    return `

        <div class="source-card">

            <div class="source-icon">
                ${
                    sourceType === "web"
                        ? "🌐"
                        : "📄"
                }
            </div>

            <div class="source-info">

                <span class="source-name">
                    ${escapeHTML(name)}
                </span>

                <span class="source-page">
                    ${escapeHTML(page)}
                </span>

            </div>

            ${link}

        </div>

    `;
}


// ============================================
// SUGGESTION BUTTON
// ============================================

function askSuggestion(
    question
) {

    questionInput.value =
        question;

    askQuestion(question);
}


// ============================================
// NEW CHAT
// ============================================

function newChat() {

    chatContainer.innerHTML = `

        <div
            id="welcome"
            class="welcome"
        >

            <div class="welcome-icon">
                🎓
            </div>

            <h2>
                How can I help you?
            </h2>

            <p>
                Ask questions about college rules,
                admissions, attendance, regulations,
                notices and more.
            </p>

            <div class="suggestions">

                <button
                    onclick="askSuggestion(
                        'What is the attendance requirement?'
                    )"
                >
                    <span>📅</span>

                    <div>
                        <strong>Attendance</strong>

                        <small>
                            What is the attendance requirement?
                        </small>
                    </div>
                </button>


                <button
                    onclick="askSuggestion(
                        'What documents are required for admission?'
                    )"
                >
                    <span>📋</span>

                    <div>
                        <strong>Admission</strong>

                        <small>
                            Required admission documents
                        </small>
                    </div>
                </button>


                <button
                    onclick="askSuggestion(
                        'What are the college examination rules?'
                    )"
                >
                    <span>📝</span>

                    <div>
                        <strong>Examination</strong>

                        <small>
                            College examination rules
                        </small>
                    </div>
                </button>


                <button
                    onclick="askSuggestion(
                        'What are the latest UGC regulations?'
                    )"
                >
                    <span>🌐</span>

                    <div>
                        <strong>Current Information</strong>

                        <small>
                            Latest UGC regulations
                        </small>
                    </div>
                </button>

            </div>

        </div>

    `;
}


// ============================================
// LOADING
// ============================================

function addLoadingMessage() {

    const id =
        "loading-" +
        Date.now();


    const message =
        document.createElement("div");


    message.className =
        "message assistant";


    message.id = id;


    message.innerHTML = `

        <div class="message-avatar">
            🎓
        </div>


        <div class="message-content">

            <div class="message-role">
                COLLEGE AI
            </div>

            <div class="message-bubble">

                <div class="loading">

                    <span></span>
                    <span></span>
                    <span></span>

                    <span style="
                        margin-left:6px;
                        background:none;
                        width:auto;
                        height:auto;
                        color:#667085;
                        animation:none;
                    ">
                        Searching...
                    </span>

                </div>

            </div>

        </div>

    `;


    chatContainer.appendChild(
        message
    );


    scrollToBottom();


    return id;
}


function removeLoadingMessage(id) {

    const element =
        document.getElementById(id);


    if (element) {
        element.remove();
    }
}


// ============================================
// INPUT LOADING STATE
// ============================================

function setLoading(
    loading
) {

    questionInput.disabled =
        loading;

    sendBtn.disabled =
        loading;

    uploadBtn.disabled =
        loading;
}


// ============================================
// AUTO RESIZE TEXTAREA
// ============================================

questionInput.addEventListener(
    "input",
    autoResize
);


function autoResize() {

    questionInput.style.height =
        "auto";

    questionInput.style.height =
        Math.min(
            questionInput.scrollHeight,
            120
        ) + "px";
}


// ============================================
// ENTER TO SEND
// ============================================

questionInput.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            chatForm.requestSubmit();
        }
    }
);


// ============================================
// SCROLL
// ============================================

function scrollToBottom() {

    setTimeout(() => {

        chatContainer.scrollTo({
            top:
                chatContainer.scrollHeight,

            behavior:
                "smooth"
        });

    }, 50);
}


// ============================================
// FORMAT ANSWER
// ============================================

function formatAnswer(text) {

    if (!text) {
        return "";
    }


    let formatted =
        escapeHTML(text);


    // Bold

    formatted =
        formatted.replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        );


    // Line breaks

    formatted =
        formatted.replace(
            /\n/g,
            "<br>"
        );


    return formatted;
}


// ============================================
// SECURITY HELPERS
// ============================================

function escapeHTML(
    value
) {

    if (value === null ||
        value === undefined) {

        return "";
    }


    return String(value)
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );
}


function escapeAttribute(
    value
) {

    return escapeHTML(value);
}