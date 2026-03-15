document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');
  
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    // Clear previous errors
    const container = document.getElementById('messages-container');
    container.innerHTML = '';
    
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    
    try {
      console.log('Sending login request...'); // DEBUG
      
      const response = await fetch('/admin/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ email, password }),
      });
      
      console.log('Response status:', response.status); // DEBUG
      
      const data = await response.json();
      console.log('Response data:', data); // DEBUG
      
      if (!response.ok) {
        // ✅ SHOW ERROR - this was missing!
        showError(data.error || 'Login failed');
        return;
      }
      
      window.location.href = '/admin/';
      
    } catch (error) {
      showError('Network error. Please try again.');
      console.error('Fetch error:', error);
    }
  });
});

function showError(message) {
  const container = document.getElementById('messages-container');
  const alert = document.createElement('div');
  alert.className = 'alert alert-danger alert-dismissible fade show mb-3';
  alert.innerHTML = `
    <i class="bi bi-exclamation-triangle-fill me-2"></i>
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  `;
  container.appendChild(alert);
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
