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

document.addEventListener('DOMContentLoaded', function() {
  const dropdown = document.getElementById('categoriesDropdown');
  
  fetch('/api/categories/')
    .then(response => response.json())
    .then(data => {
      dropdown.innerHTML = ''; // Clear "loading..." message
      if (data.categories && data.categories.length > 0) {
        data.categories.forEach(category => {
          const li = document.createElement('li');
          const a = document.createElement('a');
          a.className = 'dropdown-item';
          a.href = `/products/${category.id}/`;
          a.textContent = category.name;
          li.appendChild(a);
          dropdown.appendChild(li);
        });
      } else {
        const p = document.createElement('p');
        p.className = 'text-danger cat-err';
        p.textContent = 'Categories not found yet.';
        dropdown.appendChild(p);
      }
    })
    .catch(error => {
      dropdown.innerHTML = '';
      const p = document.createElement('p');
      p.className = 'text-danger cat-err';
      p.textContent = 'Failed to load categories.';
      dropdown.appendChild(p);
      console.error('Error fetching categories:', error);
    });
});