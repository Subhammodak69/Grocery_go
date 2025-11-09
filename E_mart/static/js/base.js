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


     const searchInput = document.getElementById('search-input');
  const resultDiv = document.getElementById('result');

  searchInput.addEventListener('input', function() {
    const query = this.value.trim();

    if (query.length === 0) {
      resultDiv.innerHTML = '';
      return;
    }

    fetch(`/api/products/search?q=${encodeURIComponent(query)}`)
      .then(response => response.json())
      .then(data => {
        if (data.length === 0) {
          resultDiv.innerHTML = '<p class="p-2">No products found.</p>';
          return;
        }

        let html = '';
        data.forEach(product => {
          html += `<div class="p-2 border-bottom" onclick="window.location.href='/products/${product.category_id}/'">
                      <strong>${product.product_name}</strong><br/>
                      <small>${product.category_name}</small>
                  </div>`;
        });

        resultDiv.innerHTML = html;
      })
      .catch(error => {
        resultDiv.innerHTML = '<p class="p-2 text-danger">Error fetching results.</p>';
        console.error('Search error:', error);
      });
  });

  document.addEventListener('click', function(event) {
    const isClickInside = searchInput.contains(event.target);

    if (!isClickInside) { // Clicked outside the input
      searchInput.value = '';
      resultDiv.innerHTML = '';
    }
  });

});


