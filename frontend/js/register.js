const registerBtn = document.getElementById("registerBtn");

const usernameInput =
    document.getElementById("registerUsername");

const emailInput =
    document.getElementById("registerEmail");

const passwordInput =
    document.getElementById("registerPassword");

const message =
    document.getElementById("registerMessage");


registerBtn.addEventListener("click", async function () {

    const username = usernameInput.value.trim();
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();


    // Check fields
    if (!username || !email || !password) {

        message.textContent =
            "Please fill all fields.";

        return;
    }


    message.textContent =
        "Creating account...";


    try {

        const response = await fetch(
            "http://127.0.0.1:5000/register",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.error || "Registration failed."
            );

        }


        message.textContent =
            "Account created successfully!";


        // Clear fields
        usernameInput.value = "";
        emailInput.value = "";
        passwordInput.value = "";


        // Go back to login after 1.5 seconds
        setTimeout(function () {

            window.location.href = "/pages/login.html";

        }, 1500);


    } catch (error) {

        console.error(error);

        message.textContent =
            "Error: " + error.message;

    }

});