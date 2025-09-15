document.addEventListener('DOMContentLoaded', () => {
  // Make all functions global so onclick can access them
  const loader = document.getElementById('loaderdiv');
  const resTrue = document.getElementById('result-true');
  const resFalse = document.getElementById('result-false');
  
  window.sendOtp = function() {
    const email = document.getElementById('email').value;

    if (!email) {
        alert('Please enter email');
      return;
    }
    loader.style.display = 'block ';

    fetch('/send-otp/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({
        email: email,
        purpose: 'login'
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.message === 'OTP sent successfully') {
        loader.style.display = 'none ';
        resFalse.style.display = "none";
        resTrue.style.display = "flex";
        resTrue.innerHTML = data.message;
        document.getElementById('otpSection').classList.remove('d-none');
        document.getElementById('sendOtpBtn').classList.add('d-none');
      } else {
        loader.style.display = 'none ';
        resTrue.style.display = "none";
        resFalse.style.display = "flex";
        resFalse.innerHTML = data.message;
      }
    })
    .catch(error => {
      loader.style.display = 'none ';
      resFalse.style.display = "flex";
      resTrue.style.display = "none";
      resFalse.innerHTML = error;
    });
  };

  window.resendOtp = function() {
    const email = document.getElementById('email').value;
    loader.style.display = 'block ';

    fetch('/send-otp/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({ email: email, purpose: 'login' }),
    })
    .then(response => response.json())
    .then(data => {
      loader.style.display = 'none ';
      resFalse.style.display = "none";
      resTrue.style.display = "flex";
      resTrue.innerHTML = data.message;
    })
    .catch(error => {
      loader.style.display = 'none ';
      resFalse.style.display = "flex";
      resTrue.style.display = "none";
      resFalse.innerHTML = error;
    });
  };

  window.verifyOtp = function() {
    const email = document.getElementById('email').value;
    const otp = document.getElementById('otp').value;

    if (!otp) {
      alert('Please enter OTP');
      return;
    }

    fetch('/verify-otp/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({ email: email, otp: otp }),
    })
    .then(response => response.json())
    .then(data => {
      if (data.message === 'verified') {
        resFalse.style.display = "none";
        resTrue.style.display = "flex";
        resTrue.innerHTML = "OTP verified successfully";
        setTimeout(()=>{
          login(email);
        },1000
        ) 

        document.getElementById('otpSection').classList.add('d-none');
      } else {
        loader.style.display = 'none ';
        resTrue.style.display = "none";
        resFalse.style.display = "flex";
        resFalse.innerHTML = data.message || "OTP Verification failed!";
      }
    })
    .catch(error => {
        loader.style.display = 'none ';
        resTrue.style.display = "none";
        resFalse.style.display = "flex";
        resFalse.innerHTML = error;
    });
  };


  function login(email) {
    fetch('/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({ email: email }),
    })
    .then(response => response.json())
    .then(data => {
      if (data.message === 'Login Successfully') {
        resFalse.style.display = "none";
        resTrue.style.display = "flex";
        resTrue.innerHTML = data.message;
        setTimeout(()=>{
           window.location.href='/';
        },1000)
       
      } else {
        resFalse.style.display = "flex";
        resTrue.style.display = "none";
        resFalse.innerHTML = data.message;
      }
    })
    .catch(error => {
      resFalse.style.display = "flex";
      resTrue.style.display = "none";
      resFalse.innerHTML = error;
    });
  }

 
  // Utility function to retrieve CSRF token cookie
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
