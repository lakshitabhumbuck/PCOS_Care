// ===============================
// LOGIN & SIGNUP POPUPS
// ===============================

// Elements
const loginModal = document.getElementById("loginModal");
const signupModal = document.getElementById("signupModal");

const loginBtn = document.querySelector(".login-btn"); // navbar Login button

// Open Login Popup
loginBtn.onclick = () => {
    loginModal.style.display = "flex";
    signupModal.style.display = "none";
};

// Open Signup Popup (from footer link)
function openSignup() {
    signupModal.style.display = "flex";
    loginModal.style.display = "none";
}

// Open Login Popup (from signup footer link)
function openLogin() {
    loginModal.style.display = "flex";
    signupModal.style.display = "none";
}

// Close popup when clicking outside
window.onclick = function (e) {
    if (e.target.classList.contains("modal")) {
        e.target.style.display = "none";
    }
};


// ===============================
// OPTIONAL: Save username and show "Welcome, User"
// (Frontend dummy login system)
// ===============================

const loginButtonInside = document.querySelector("#loginModal .modal-btn");

if (loginButtonInside) {
    loginButtonInside.addEventListener("click", () => {
        const emailInput = document.querySelector("#loginModal input[type='email']");
        let username = emailInput.value.split("@")[0]; // extract name before @

        localStorage.setItem("pcosUser", username);
        alert("Welcome, " + username + "! You are logged in.");
        loginModal.style.display = "none";
        updateNavbarUser();
    });
}

function updateNavbarUser() {
    let user = localStorage.getItem("pcosUser");

    if (user) {
        const navLinks = document.querySelector(".nav-links");
        navLinks.innerHTML = `
            <a href="index.html">Home</a>
            <a href="assessment.html">Assessment</a>
            <span class="login-btn" style="background:#ff3e8d;">Welcome, ${user}</span>
        `;
    }
}
// Switch between Login & Signup
document.querySelector(".switch-to-signup").onclick = () => {
    loginPopup.style.display = "none";
    signupPopup.style.display = "flex";
};

document.querySelector(".switch-to-login").onclick = () => {
    signupPopup.style.display = "none";
    loginPopup.style.display = "flex";
};


// Run on page load
updateNavbarUser();
