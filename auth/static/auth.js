// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {

  // 1: Toggle password visibility
  const togglePasswordButtons = document.querySelectorAll('.toggle-password');
  
  togglePasswordButtons.forEach(button => {
      button.addEventListener('click', function() {
          const input = this.previousElementSibling;
          const icon = this.querySelector('i');
          
          if (input.type === 'password') {
              input.type = 'text';
              icon.classList.remove('fa-eye');
              icon.classList.add('fa-eye-slash');
          } else {
              input.type = 'password';
              icon.classList.remove('fa-eye-slash');
              icon.classList.add('fa-eye');
          }
      });
  });

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
  
})