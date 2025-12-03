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
// TOAST FUNCTION
// =======================
function showToast(message, type = "info", duration = 3000) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.className = `toast show ${type}`;

  setTimeout(() => {
    toast.className = "toast";
  }, duration);
}

// =======================
// AUTH FORM SUBMISSION
// =======================
document.addEventListener("DOMContentLoaded", () => {

  // ---------- LOGIN ----------
  const loginForm = document.getElementById("loginForm");
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
        if (result.success) {
          showToast(result.message, "success");
          if (result.redirect) {
            setTimeout(() => {
              window.location.href = result.redirect;
            }, 1500);
          }
        } else {
          showToast(result.message || "Login failed. Try again.", "error");
        }

      } catch (err) {
        console.error(err);
        showToast("Server error. Try again later.", "error");
      }
    });
  }

  // ---------- REGISTER ----------
  const registerForm = document.getElementById("registerForm");
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
        if (result.success) {
          showToast(result.message, "success");
          if (result.redirect) {
            setTimeout(() => {
              window.location.href = result.redirect;
            }, 1500);
          }
        } else {
          showToast(result.message || "Registration failed. Try again.", "error");
        }

      } catch (err) {
        console.error(err);
        showToast("Server error. Try again later.", "error");
      }
    });
  }

  // ---------- LOGOUT ----------
//   // ---------- LOGOUT ----------
// const logoutLink = document.getElementById("logoutLink");
// if (logoutLink) {
//   logoutLink.addEventListener("click", async (e) => {
//     e.preventDefault();

//     // disable the link temporarily to prevent double clicks
//     logoutLink.style.pointerEvents = "none";

//     try {
//       const response = await fetch("/logout", { method: "GET" });
//       const result = await response.json();

//       if (result.success) {
//         showToast(result.message, "success");
//         setTimeout(() => {
//           window.location.href = result.redirect;
//         }, 1500);
//       } else {
//         showToast(result.message || "Failed to logout. Try again.", "error");
//       }

//     } catch (err) {
//       console.error("Logout error:", err);
//       showToast("Server error. Try again later.", "error");
//     } finally {
//       // re-enable link after 2 seconds
//       setTimeout(() => {
//         logoutLink.style.pointerEvents = "auto";
//       }, 2000);
//     }
//   });
// }

["logoutDropdown", "logoutSidebar"].forEach(id => {
  const logoutLink = document.getElementById(id);
  if (logoutLink) {
    logoutLink.addEventListener("click", async (e) => {
      e.preventDefault();
      try {
        const response = await fetch("/logout", { method: "GET" });
        const result = await response.json();
        if (result.success) {
          showToast(result.message, "success");
          setTimeout(() => {
            window.location.href = result.redirect;
          }, 1500);
        } else {
          showToast("Failed to logout. Try again.", "error");
        }
      } catch (err) {
        console.error("Logout error:", err);
        showToast("Server error. Try again later.", "error");
      }
    });
  }
});


  // ---------- NAV LINK ACTIVE STATE ----------
  const navLinks = document.querySelectorAll(".nav-menu .link");
  navLinks.forEach(link => {
    link.addEventListener("click", function() {
      navLinks.forEach(l => l.classList.remove("active"));
      this.classList.add("active");
    });
  });

});
