// =======================
// NAV MENU TOGGLE
// =======================
function myMenuFunction() {
  const navMenu = document.getElementById("navMenu");
  navMenu.className = navMenu.className === "nav-menu" ? "nav-menu responsive" : "nav-menu";
}

// =======================
// SWITCH LOGIN / REGISTER
// =======================
const loginBtn = document.getElementById("loginBtn");
const registerBtn = document.getElementById("registerBtn");
const loginDiv = document.getElementById("login");
const registerDiv = document.getElementById("register");

function login() {
  loginDiv.style.left = "4px";
  registerDiv.style.right = "-520px";
  loginBtn.classList.add("white-btn");
  registerBtn.classList.remove("white-btn");
  loginDiv.style.opacity = 1;
  registerDiv.style.opacity = 0;
}

function register() {
  loginDiv.style.left = "-510px";
  registerDiv.style.right = "5px";
  loginBtn.classList.remove("white-btn");
  registerBtn.classList.add("white-btn");
  loginDiv.style.opacity = 0;
  registerDiv.style.opacity = 1;
}

// =======================
// AUTH FORM SUBMISSION
// =======================
document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");

  const showMessage = (msg) => alert(msg); // optional: replace with inline flash messages

  // ---------- LOGIN ----------
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const data = {
        school_id: document.getElementById("loginSchoolId").value.trim(),
        password: document.getElementById("loginPassword").value.trim(),
        role: document.getElementById("loginRole").value,
        remember: document.getElementById("loginCheck").checked
      };

      try {
        const response = await fetch("/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });

        const result = await response.json();
        showMessage(result.message);
        if (result.success && result.redirect) window.location.href = result.redirect;

      } catch (err) {
        console.error(err);
        showMessage("Server error. Try again later.");
      }
    });
  }

  // ---------- REGISTER ----------
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const data = {
        school_id: document.getElementById("registerSchoolId").value.trim(),
        password: document.getElementById("registerPassword").value.trim(),
        role: document.getElementById("registerRole").value,
        remember: document.getElementById("registerCheck").checked
      };

      try {
        const response = await fetch("/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });

        const result = await response.json();
        showMessage(result.message);
        if (result.success && result.redirect) window.location.href = result.redirect;

      } catch (err) {
        console.error(err);
        showMessage("Server error. Try again later.");
      }
    });
  }


  // ----------- LOGOUT -------------
  const logoutLink = document.getElementById("logoutLink");
 console.log("print")
  if (logoutLink) {
    logoutLink.addEventListener("click", async (e) => {
      e.preventDefault(); // prevent default navigation

      try {
        const response = await fetch("/logout", { method: "GET" });
        const result = await response.json();

        if (result.success) {
          alert(result.message);             // show alert
          window.location.href = result.redirect; // redirect to login
        } else {
          alert("Failed to logout. Try again.");
        }
      } catch (err) {
        console.error("Logout error:", err);
        alert("Server error. Try again later.");
      }
    });
  }

  // ---------- NAV LINK ACTIVE STATE ----------
  const navLinks = document.querySelectorAll(".nav-menu .link");
  navLinks.forEach(link => {
    link.addEventListener("click", function() {
      navLinks.forEach(l => l.classList.remove("active"));
      this.classList.add("active");
    });
  });
});
