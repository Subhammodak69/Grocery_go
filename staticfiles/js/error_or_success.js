window.showMessage = function(type, message, redirectUrl = null) {
  const errorDiv = document.getElementById('error');
  const successDiv = document.getElementById('success');

  errorDiv.style.display = 'none';
  successDiv.style.display = 'none';

  if (type === 'success') {
    successDiv.innerText = message;
    successDiv.style.display = 'block';
    setTimeout(() => {
      successDiv.style.display = 'none';
      if (redirectUrl) {
        window.location.href = redirectUrl;
      }
    }, 2000);  // Show message for 2 seconds, then hide and redirect
  } else if (type === 'error') {
    errorDiv.innerText = message;
    errorDiv.style.display = 'block';
    setTimeout(() => {
      errorDiv.style.display = 'none';
    }, 2000);
  }
};
