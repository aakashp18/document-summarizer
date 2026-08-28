const loginBtn = document.getElementById("loginBtn");

const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");


loginBtn.addEventListener("click", async function () {

    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    if (!username || !password) {

        alert("Please enter username and password.");

        return;
    }

    loginBtn.disabled = true;
    loginBtn.textContent = "Logging in...";

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/login",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    login: username,
                    password: password
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.error || "Login failed."
            );
        }

        // ========================================
        // SAVE JWT TOKEN
        // ========================================

        localStorage.setItem(
            "token",
            data.token
        );


        // ========================================
        // SAVE USER INFORMATION
        // ========================================

        localStorage.setItem(
            "user",
            JSON.stringify(data.user)
        );


        // ========================================
        // OPEN SUMMARIZER
        // ========================================

        window.location.href = "/pages/app.html";


    } catch (error) {

        console.error(error);

        alert(error.message);

    } finally {

        loginBtn.disabled = false;
        loginBtn.textContent = "Login";
    }

});