document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');
  
  form.addEventListener('submit', async (event) => {
    event.preventDefault(); // prevent page reload
    
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    
    try {
      const response = await fetch('/admin/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': 'csrftoken'
        },
        body: JSON.stringify({ email, password }),
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.log('Error details:', errorData);
        return;
      }
      
      const data = await response.json();
      alert('Login successful:', data);
      window.location.href='/admin/';
      
    } catch (error) {
      console.error('Error during login fetch:', error);
    }
  });
});
