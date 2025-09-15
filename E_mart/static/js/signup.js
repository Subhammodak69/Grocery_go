// signup.js
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
        purpose: 'signup'
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
        loader.style.display = 'none ';
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
      body: JSON.stringify({ email: email, purpose: 'signup' }),
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
    loader.style.display = 'block';
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
        document.getElementById('userDataSection').classList.remove('d-none');
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

  window.next = function() {
    const firstName = document.getElementById('first_name').value;
    const lastName = document.getElementById('last_name').value;
    const phoneNumber = document.getElementById('phone_number').value;

    if (!firstName || !lastName || !phoneNumber) {
      alert('Please fill all required fields');
      return;
    }

    document.getElementById('addressDiv').classList.remove('d-none');
    document.getElementById('userDataSection').classList.add('d-none');
  };

  window.signup = function() {
    const email = document.getElementById('email').value;
    const firstName = document.getElementById('first_name').value;
    const lastName = document.getElementById('last_name').value;
    const phoneNumber = document.getElementById('phone_number').value;
    const address = document.getElementById('address').value;

    if (!email || !firstName || !lastName || !phoneNumber) {
      alert('Please fill all required fields');
      return;
    }
    loader.style.display = 'block';
    fetch('/signup/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({
        email: email,
        first_name: firstName,
        last_name: lastName,
        phone: phoneNumber,
        address: address
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.message === 'Signup completed') {
        loader.style.display = 'none ';
        resFalse.style.display = "none";
        resTrue.style.display = "flex";
        resTrue.innerHTML = data.message;
        setTimeout(()=>{
           window.location.href = '/'; 
        },1000)
      }else{
        loader.style.display = 'none ';
        resFalse.style.display = "flex";
        resTrue.style.display = "none";
        resFalse.innerHTML = data.message;
      }
    })
    .catch(error => {
        loader.style.display = 'none ';
        resTrue.style.display = "none";
        resFalse.style.display = "flex";
        resFalse.innerHTML = error;
    });
  };

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
