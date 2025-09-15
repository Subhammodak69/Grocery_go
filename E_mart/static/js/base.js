document.addEventListener('DOMContentLoaded', () => {
    const loader = document.getElementById('loaderdiv');
    window.logout = function(){
        loader.style.display = 'block ';
        fetch('/logout/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .finally(() => {
            setTimeout(() => {
                loader.style.display = 'none ';
                window.location.href = '/';
            }, 2000);
        });
    }
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

})

