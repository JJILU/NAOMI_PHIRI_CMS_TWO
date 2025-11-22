
function myMenuFunction() {
  var i = document.getElementById("navMenu")

  if (i.className === "nav-menu") {
    i.className += " responsive";
  } else {
    i.className = "nav-menu";
  }
}

var a = document.getElementById("loginBtn");
var b = document.getElementById("registerBtn");
var x = document.getElementById("login");
var y = document.getElementById("register");

function login() {
  x.style.left = "4px";
  y.style.right = "-520px";
  a.className += " white-btn";
  b.className = "btn";
  x.style.opacity = 1;
  y.style.opacity  = 0;
}

function register() {
  x.style.left = "-510px";
  y.style.right = "5px";
  a.className = "btn";
  b.className += " white-btn";
  x.style.opacity= 0;
  y.style.opacity = 1;
}


// -------------------- Auth Logic -------------------------------
document.addEventListener('DOMContentLoaded', () => {
  // --- LOGIN FORM ---
  const loginForm = document.getElementById('loginForm'); 
  const registerForm = document.getElementById('registerForm');

  if (loginForm) {
  const loginMsg = document.createElement('p');
  loginMsg.style.textAlign = 'center';
  loginMsg.style.color = '#fff';
  // loginMsg.style.height = '20px';
  // loginMsg.style.padding = '2px';
  loginForm.prepend(loginMsg); // show message above inputs

  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
      school_id: document.getElementById('loginSchoolId').value.trim(),
      password: document.getElementById('loginPassword').value.trim(),
      role: document.getElementById('loginRole').value,
      remember: document.getElementById('loginCheck').checked
    };

    try {
      const response = await fetch('/', {  // replace with your Flask route
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();

      if (result.success) {
        loginMsg.textContent = result.success;
        loginMsg.style.color = 'lightgreen';
        setTimeout(() => {
          window.location.href = result.redirect_url;
        }, 1000);
      } else {
        loginMsg.textContent = result.error;
        loginMsg.style.color = 'red';
      }

    } catch (err) {
      loginMsg.textContent = 'Server error. Try again later.';
      loginMsg.style.color = 'red';
      console.error(err);
    }
  });
}

  // --- REGISTRATION FORM ---
  if (registerForm) {
  const registerMsg = document.createElement('p');
  registerMsg.style.textAlign = 'center';
  registerMsg.style.color = '#fff';
  // registerMsg.style.height = '20px';
  // registerMsg.style.padding = '2px';
  registerForm.prepend(registerMsg);

  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
      school_id: document.getElementById('registerSchoolId').value.trim(),
      password: document.getElementById('registerPassword').value.trim(),
      role: document.getElementById('registerRole').value,
      remember: document.getElementById('registerCheck').checked
    };

    try {
      const response = await fetch('/register', {  // replace with your Flask route
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();

      if (result.success) {
        console.log(result.success)
        registerMsg.textContent = result.success;
        registerMsg.style.color = 'lightgreen';
        setTimeout(() => {
          window.location.href = result.redirect_url;
        }, 1000);
      } else {
        console.log(result.error)
        registerMsg.textContent = result.error;
        registerMsg.style.color = 'red';
      }

    } catch (err) {
      registerMsg.textContent = 'Server error. Try again later.';
      registerMsg.style.color = 'red';
      console.error(err);
    }
  });
}

});


// ======== nav menu ========
 // Select all links in the nav
 document.addEventListener('DOMContentLoaded', () => {
  const navLinks = document.querySelectorAll('.nav-menu .link');

  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      // Optional: prevent page reload if using "#" links
      // e.preventDefault();

      navLinks.forEach(l => l.classList.remove('active'));
      this.classList.add('active');
    });
  });
});