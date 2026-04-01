// ----- REGISTER -----
const registerBtn = document.getElementById("register-btn");
const regErrorText = document.getElementById("reg-error-text");

if (registerBtn) {
    registerBtn.addEventListener("click", function () {
        const username = document.getElementById("reg-username").value.trim();
        const password = document.getElementById("reg-password").value.trim();

        if (username === "" || password === "") {
            regErrorText.textContent = "Please enter username and password.";
            regErrorText.style.display = "block";
            return;
        }

        // Save account in localStorage (demo only)
        const users = JSON.parse(localStorage.getItem("users") || "[]");

        // Check if username exists
        if (users.find(user => user.username === username)) {
            regErrorText.textContent = "Username already exists!";
            regErrorText.style.display = "block";
            return;
        }

        users.push({ username, password });
        localStorage.setItem("users", JSON.stringify(users));

        alert("Registration successful!");
        window.location.href = "login.html"; // go to login
    });
}

// ----- LOGIN -----
const loginBtn = document.getElementById("login-btn");
const errorText = document.getElementById("error-text");

if (loginBtn) {
    loginBtn.addEventListener("click", function () {
        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();

        if (username === "" || password === "") {
            errorText.textContent = "Please enter username and password.";
            errorText.style.display = "block";
            return;
        }

        const users = JSON.parse(localStorage.getItem("users") || "[]");
        const user = users.find(u => u.username === username && u.password === password);

        if (!user) {
            errorText.textContent = "Invalid username or password.";
            errorText.style.display = "block";
            return;
        }

        errorText.style.display = "none";
        localStorage.setItem("currentUser", username);

        alert("Login successful!");
        window.location.href = "dashboard.html";
    });
}

// ----- DASHBOARD -----
const welcomeMsg = document.getElementById("welcome-msg");
if (welcomeMsg) {
    const currentUser = localStorage.getItem("currentUser");
    if (currentUser) {
        welcomeMsg.textContent = `Welcome, ${currentUser}!`;
    } else {
        window.location.href = "login.html"; // if not logged in, go back
    }
}

// ----- LOGOUT -----
const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
    logoutBtn.addEventListener("click", function() {
        localStorage.removeItem("currentUser");
        alert("You are logged out!");
        window.location.href = "login.html";
    });
}