// ======================================================
// API
// ======================================================

const API_URL = "http://127.0.0.1:5000";


// ======================================================
// AUTHENTICATION
// ======================================================

const TOKEN = localStorage.getItem("token");
const USER_DATA = localStorage.getItem("user");


// ======================================================
// GET ELEMENTS
// ======================================================

const plusBtn = document.getElementById("plusBtn");
const plusMenu = document.getElementById("plusMenu");

const documentOption =
    document.getElementById("documentOption");

const imageOption =
    document.getElementById("imageOption");

const documentInput =
    document.getElementById("documentInput");

const imageInput =
    document.getElementById("imageInput");

const textInput =
    document.getElementById("textInput");

const selectedFile =
    document.getElementById("selectedFile");

const fileName =
    document.getElementById("fileName");

const fileIcon =
    document.getElementById("fileIcon");

const removeFileBtn =
    document.getElementById("removeFileBtn");

const imagePreviewContainer =
    document.getElementById("imagePreviewContainer");

const imagePreview =
    document.getElementById("imagePreview");

const imageName =
    document.getElementById("imageName");

const removeImageBtn =
    document.getElementById("removeImageBtn");

const summarizeBtn =
    document.getElementById("summarizeBtn");

const loading =
    document.getElementById("loading");

const error =
    document.getElementById("error");

const result =
    document.getElementById("result");

const summaryText =
    document.getElementById("summaryText");

const closeResultBtn =
    document.getElementById("closeResultBtn");

const recentSummaries =
    document.getElementById("recentSummaries");

const accountBtn =
    document.getElementById("accountBtn");



const newChatBtn =
    document.getElementById("newChatBtn");



// ======================================================
// SIDEBAR COLLAPSE
// ======================================================

const appLayout =
    document.querySelector(".app-layout");

const collapseSidebarBtn =
    document.getElementById("collapseSidebarBtn");

const openSidebarBtn =
    document.getElementById("openSidebarBtn");


if (
    appLayout &&
    collapseSidebarBtn &&
    openSidebarBtn
) {

    collapseSidebarBtn.addEventListener(
        "click",
        function () {

            appLayout.classList.add(
                "sidebar-collapsed"
            );

        }
    );


    openSidebarBtn.addEventListener(
        "click",
        function () {

            appLayout.classList.remove(
                "sidebar-collapsed"
            );

        }
    );

}

// ======================================================
// SELECTED FILE STATE
// ======================================================

let selectedDocument = null;
let selectedImage = null;


// ======================================================
// PLUS BUTTON
// ======================================================

if (plusBtn && plusMenu) {

    plusBtn.addEventListener("click", function (event) {

        event.stopPropagation();

        plusMenu.classList.toggle("hidden");

    });

}


// ======================================================
// CLOSE PLUS MENU
// ======================================================

document.addEventListener("click", function (event) {

    if (
        plusBtn &&
        plusMenu &&
        !plusBtn.contains(event.target) &&
        !plusMenu.contains(event.target)
    ) {

        plusMenu.classList.add("hidden");

    }

});


// ======================================================
// DOCUMENT OPTION
// ======================================================

if (documentOption && documentInput) {

    documentOption.addEventListener(
        "click",
        function () {

            plusMenu.classList.add("hidden");

            documentInput.click();

        }
    );

}


// ======================================================
// PICTURE OPTION
// ======================================================

if (imageOption && imageInput) {

    imageOption.addEventListener(
        "click",
        function () {

            plusMenu.classList.add("hidden");

            imageInput.click();

        }
    );

}


// ======================================================
// DOCUMENT SELECTED
// ======================================================

if (documentInput) {

    documentInput.addEventListener(
        "change",
        function () {

            if (!documentInput.files.length) {
                return;
            }

            selectedDocument =
                documentInput.files[0];

            // Remove selected picture
            selectedImage = null;

            imageInput.value = "";

            imagePreviewContainer.classList.add(
                "hidden"
            );


            // Show document

            fileName.textContent =
                selectedDocument.name;

            fileIcon.textContent =
                "📄";

            selectedFile.classList.remove(
                "hidden"
            );


            updateSummarizeButton();

        }
    );

}


// ======================================================
// PICTURE SELECTED
// ======================================================

if (imageInput) {

    imageInput.addEventListener(
        "change",
        function () {

            if (!imageInput.files.length) {
                return;
            }

            selectedImage =
                imageInput.files[0];

            // Remove selected document
            selectedDocument = null;

            documentInput.value = "";

            selectedFile.classList.add(
                "hidden"
            );


            // Show image

            imageName.textContent =
                selectedImage.name;

            const imageURL =
                URL.createObjectURL(
                    selectedImage
                );

            imagePreview.src =
                imageURL;

            imagePreviewContainer.classList.remove(
                "hidden"
            );


            updateSummarizeButton();

        }
    );

}


// ======================================================
// REMOVE DOCUMENT
// ======================================================

if (removeFileBtn) {

    removeFileBtn.addEventListener(
        "click",
        function () {

            selectedDocument = null;

            documentInput.value = "";

            selectedFile.classList.add(
                "hidden"
            );

            updateSummarizeButton();

        }
    );

}


// ======================================================
// REMOVE PICTURE
// ======================================================

if (removeImageBtn) {

    removeImageBtn.addEventListener(
        "click",
        function () {

            selectedImage = null;

            imageInput.value = "";

            imagePreview.src = "";

            imagePreviewContainer.classList.add(
                "hidden"
            );

            updateSummarizeButton();

        }
    );

}


// ======================================================
// TEXT INPUT
// ======================================================

if (textInput) {

    textInput.addEventListener(
        "input",
        function () {

            updateSummarizeButton();

        }
    );

}


// ======================================================
// SHOW / HIDE SUMMARIZE BUTTON
// ======================================================

function updateSummarizeButton() {

    const hasText =
        textInput &&
        textInput.value.trim().length > 0;

    const hasDocument =
        selectedDocument !== null;

    const hasImage =
        selectedImage !== null;


    if (
        hasText ||
        hasDocument ||
        hasImage
    ) {

        summarizeBtn.classList.remove(
            "hidden"
        );

    } else {

        summarizeBtn.classList.add(
            "hidden"
        );

    }

}


// ======================================================
// SUMMARIZE
// ======================================================

if (summarizeBtn) {

    summarizeBtn.addEventListener(
        "click",
        async function () {

            hideError();

            hideResult();

            showLoading();


            try {

                // --------------------------------------
                // DOCUMENT
                // --------------------------------------

                if (selectedDocument) {

                    await summarizeDocument();

                    return;

                }


                // --------------------------------------
                // PICTURE
                // --------------------------------------

                if (selectedImage) {

                    await summarizeImage();

                    return;

                }


                // --------------------------------------
                // TEXT
                // --------------------------------------

                const text =
                    textInput.value.trim();

                if (!text) {

                    throw new Error(
                        "Please enter some text."
                    );

                }

                await summarizeText(text);

            } catch (err) {

                console.error(err);

                showError(
                    err.message ||
                    "Something went wrong."
                );

            } finally {

                hideLoading();

            }

        }
    );

}


// ======================================================
// SUMMARIZE TEXT
// ======================================================

async function summarizeText(text) {

    const headers = {
        "Content-Type": "application/json"
    };


    if (TOKEN) {

        headers["Authorization"] =
            `Bearer ${TOKEN}`;

    }


    const response =
        await fetch(
            `${API_URL}/summarize-text`,
            {
                method: "POST",

                headers: headers,

                body: JSON.stringify({
                    text: text
                })
            }
        );


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            data.error ||
            "Text summarization failed."
        );

    }


    showSummary(
        data.summary
    );

}


// ======================================================
// SUMMARIZE DOCUMENT
// ======================================================

async function summarizeDocument() {

    const formData =
        new FormData();

    formData.append(
        "file",
        selectedDocument
    );


    const headers = {};


    if (TOKEN) {

        headers["Authorization"] =
            `Bearer ${TOKEN}`;

    }


    const response =
        await fetch(
            `${API_URL}/summarize-file`,
            {
                method: "POST",

                headers: headers,

                body: formData
            }
        );


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            data.error ||
            "Document summarization failed."
        );

    }


    showSummary(
        data.summary
    );

}


// ======================================================
// SUMMARIZE PICTURE
// ======================================================

async function summarizeImage() {

    const formData =
        new FormData();

    formData.append(
        "file",
        selectedImage
    );


    const headers = {};


    if (TOKEN) {

        headers["Authorization"] =
            `Bearer ${TOKEN}`;

    }


    const response =
        await fetch(
            `${API_URL}/summarize-image`,
            {
                method: "POST",

                headers: headers,

                body: formData
            }
        );


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            data.error ||
            "Picture summarization failed."
        );

    }


    showSummary(
        data.summary
    );

}


// ======================================================
// SHOW SUMMARY
// ======================================================

function showSummary(summary) {

    summaryText.textContent =
        summary;

    result.classList.remove(
        "hidden"
    );


    // Refresh recent history
    loadRecentSummaries();

}


// ======================================================
// CLOSE RESULT
// ======================================================

if (closeResultBtn) {

    closeResultBtn.addEventListener(
        "click",
        function () {

            hideResult();

        }
    );

}


// ======================================================
// NEW CHAT
// ======================================================

if (newChatBtn) {

    newChatBtn.addEventListener(
        "click",
        function () {

            clearInput();

            hideResult();

            hideError();

        }
    );

}


// ======================================================
// CLEAR INPUT
// ======================================================

function clearInput() {

    if (textInput) {

        textInput.value = "";

    }


    selectedDocument = null;

    selectedImage = null;


    if (documentInput) {

        documentInput.value = "";

    }


    if (imageInput) {

        imageInput.value = "";

    }


    if (selectedFile) {

        selectedFile.classList.add(
            "hidden"
        );

    }


    if (imagePreviewContainer) {

        imagePreviewContainer.classList.add(
            "hidden"
        );

    }


    if (imagePreview) {

        imagePreview.src = "";

    }


    updateSummarizeButton();

}


// ======================================================
// ACCOUNT / SIGN IN
// ======================================================

if (accountBtn) {

    const token =
        localStorage.getItem("token");

    const userData =
        localStorage.getItem("user");


    // --------------------------------------
    // GUEST USER
    // --------------------------------------

    if (!token || !userData) {

        accountBtn.textContent =
            "🔐 Sign In";


        accountBtn.addEventListener(
            "click",
            function () {

                window.location.href =
                    "login.html";

            }
        );

    }


    // --------------------------------------
    // LOGGED-IN USER
    // --------------------------------------

    else {

        accountBtn.textContent =
            "👤 Account";


        accountBtn.addEventListener(
            "click",
            function () {

                try {

                    const user =
                        JSON.parse(userData);


                    alert(
                        "Account Information\n\n" +
                        "Username: " +
                        (user.username || "Not available") +
                        "\nEmail: " +
                        (user.email || "Not available")
                    );

                } catch (err) {

                    console.error(err);

                    alert(
                        "Unable to load account information."
                    );

                }

            }
        );

    }

}


// ======================================================
// LOGOUT
// ======================================================

const sidebarBottom =
    document.getElementById("sidebarBottom");

const logoutBtn =
    document.getElementById("logoutBtn");

const token =
    localStorage.getItem("token");

const userData =
    localStorage.getItem("user");


if (!token || !userData) {

    if (sidebarBottom) {
        sidebarBottom.remove();
    }

} else {

    logoutBtn.addEventListener("click", function () {

        const confirmLogout =
            confirm(
                "Are you sure you want to logout?"
            );

        if (!confirmLogout) {
            return;
        }

        localStorage.removeItem("token");
        localStorage.removeItem("user");

        window.location.href = "login.html";

    });

}


// ======================================================
// CHECK LOGIN STATUS
// ======================================================

// updateLogoutButton();


//             // Logged-in user
//             const confirmLogout =
//                 confirm(
//                     "Are you sure you want to logout?"
//                 );


//             if (!confirmLogout) {
//                 return;
//             }


//             localStorage.removeItem("token");

//             localStorage.removeItem("user");


//             window.location.href =
//                 "index.html";



// ======================================================
// RECENT SUMMARIES
// ======================================================

async function loadRecentSummaries() {

    if (!recentSummaries) {
        return;

    }


    const token =
        localStorage.getItem("token");


    // Guest user
    if (!token) {

        recentSummaries.innerHTML = `
            <p class="empty-history">
                Login to see recent summaries
            </p>
        `;

        return;

    }


    try {

        const response =
            await fetch(
                `${API_URL}/history`,
                {
                    method: "GET",

                    headers: {
                        "Authorization":
                            `Bearer ${token}`
                    }
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Failed to load history."
            );

        }


        const history =
            data.history || [];


        if (history.length === 0) {

            recentSummaries.innerHTML = `
                <p class="empty-history">
                    No recent summaries
                </p>
            `;

            return;

        }


        recentSummaries.innerHTML = "";


        history.forEach(
            function (item) {

                const historyItem =
                    document.createElement(
                        "div"
                    );


                historyItem.className =
                    "history-item";


                historyItem.innerHTML = `
                    <div class="history-title">
                        ${escapeHtml(
                            item.filename ||
                            "Text Summary"
                        )}
                    </div>

                    <div class="history-type">
                        ${escapeHtml(
                            item.summary_type ||
                            "standard"
                        )}
                    </div>
                `;


                historyItem.addEventListener(
                    "click",
                    function () {

                        showSummary(
                            item.summary
                        );

                    }
                );


                recentSummaries.appendChild(
                    historyItem
                );

            }
        );


    } catch (err) {

        console.error(
            "History error:",
            err
        );


        recentSummaries.innerHTML = `
            <p class="empty-history">
                Unable to load history
            </p>
        `;

    }

}


// ======================================================
// ESCAPE HTML
// ======================================================

function escapeHtml(text) {

    const div =
        document.createElement(
            "div"
        );

    div.textContent =
        text;

    return div.innerHTML;

}


// ======================================================
// UI HELPERS
// ======================================================

function showLoading() {

    if (loading) {

        loading.classList.remove(
            "hidden"
        );

    }

}


function hideLoading() {

    if (loading) {

        loading.classList.add(
            "hidden"
        );

    }

}


function showError(message) {

    if (!error) {

        return;

    }


    error.textContent =
        message;

    error.classList.remove(
        "hidden"
    );

}


function hideError() {

    if (error) {

        error.classList.add(
            "hidden"
        );

    }

}


function hideResult() {

    if (result) {

        result.classList.add(
            "hidden"
        );

    }

}


// ======================================================
// INITIALIZE
// ======================================================

updateSummarizeButton();

loadRecentSummaries();