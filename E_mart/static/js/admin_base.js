
window.onload = function() {
  const toggleBtn = document.getElementById('toggleSidebar');
  const sidebar = document.getElementById('sidebar');
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', function() {
      sidebar.classList.toggle('collapsed');
      sidebar.style.width = sidebar.classList.contains('collapsed') ? '0px' : '300px';
    });
  }
};


function change_color(value) {
  const body = document.body;
  const on = document.getElementById('on');
  const off = document.getElementById('off');

  if (value === "on") {
    body.style.background = 'white';

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
