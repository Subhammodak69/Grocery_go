function toggleWishlist(span) {
  const productId = span.getAttribute('data-product-id');
  let icon = span.querySelector('i');
  fetch(`/wishlist/toggle/${productId}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken':'csrftoken'
    }
  })
  .then(response => response.json())
  .then(data => {
    if (!data) return;
    if (data.in_wishlist) {
      icon.classList.remove('bi-heart');
      icon.classList.add('bi-heart-fill');
      icon.style.color = 'red';
    } else {
      icon.classList.remove('bi-heart-fill');
      icon.classList.add('bi-heart');
      icon.style.color = '';
    }
  })
  .catch(error => {
    window.location.href = '/login/';
  });
}


// Helper to check if a single product is in wishlist
function checkWishlist(productId) {
    return fetch(`/wishlist/check/${productId}/`)
        .then(response => response.json())
        .then(data => data.in_wishlist);
}

window.onload = function() {
    // Select all wishlist icon spans
    let spans = document.querySelectorAll('.wishlist-icon');
    spans.forEach(function(span) {
        let productId = span.getAttribute('data-product-id');
        let icon = span.querySelector('i');
        checkWishlist(productId).then(function(inWishlist) {
            if (inWishlist) {
                icon.classList.remove('bi-heart');
                icon.classList.add('bi-heart-fill');
                icon.style.color = 'red';
            } else {
                icon.classList.remove('bi-heart-fill');
                icon.classList.add('bi-heart');
                icon.style.color = '';
            }
        });
    });
};

