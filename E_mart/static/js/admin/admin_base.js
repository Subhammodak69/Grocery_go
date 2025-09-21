function change_color(value) {
  const body = document.body;
  const on = document.getElementById('on');
  const off = document.getElementById('off');

  if (value === "on") {
    body.style.background = 'white';
    body.style.color = '#000000ed';

    if (on) {
      on.classList.add('hide');
      on.classList.remove('show');
    }
    if (off) {
      off.classList.add('show');
      off.classList.remove('hide');
    }
  } else {
    body.style.background = '#272727ed';
    body.style.color = '#ffffffed';

    if (on) {
      on.classList.add('show');
      on.classList.remove('hide');
    }
    if (off) {
      off.classList.add('hide');
      off.classList.remove('show');
    }
  }
}


document.addEventListener('DOMContentLoaded', () => {
    const loader = document.getElementById('loaderdiv');
    window.logout = function(){
        loader.style.display = 'block ';
        fetch('/logout/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken':'csrftoken'
            }
        })
        .finally(() => {
            setTimeout(() => {
                loader.style.display = 'none ';
                window.location.href = '/';
            }, 2000);
        });
    }
})