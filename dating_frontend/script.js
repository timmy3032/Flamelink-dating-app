 // Selecting elements
const loginForm = document.getElementById("login-form");
const loginBtn = document.getElementById("login-btn");
const errorText = document.getElementById("error-text");

// Handle Login Button Click
loginBtn.addEventListener("click", function () {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (username === "" || password === "") {
        errorText.textContent = "Please enter username and password.";
        errorText.style.display = "block";
        return;
    }

    errorText.style.display = "none";

    // Simulating backend login (for now)
    alert("Login successful! (Frontend working)");

    // Redirect (you can change this later)
    window.location.href = "dashboard.html";
});