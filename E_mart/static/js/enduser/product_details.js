function buy_now() {
  const product_id =document.getElementById('product_id').value;
  const quantity = document.getElementById('quantity').value;

  const params = new URLSearchParams({
    product_id: product_id,
    quantity: quantity
  });
  if(!product_id){
    console.error("product_id not found");
  }
  if(!quantity){
    console.error("quantity not found");
  }
  window.location.href = `/product-order/summary/?${params.toString()}`;
}

function add_to_cart() {
  const product_id =document.getElementById('product_id').value;
  const quantity = document.getElementById('quantity').value;


  fetch('/user/cart/create-data/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      product_id: product_id,
      quantity: quantity
    })
  })
  .then(response => {
    if (response.ok) {
      window.location.href = `/user/cart/`;
    } else {
      console.error('Add to cart failed');
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });

}


function toggleWishlist(span) {
  const productId = span.getAttribute('data-product-id');
  let icon = span.querySelector('i');

  fetch(`/wishlist/toggle/${productId}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': 'csrftoken'
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




function checkWishlist(productId) {
  return fetch(`/wishlist/check/${productId}/`)
    .then(response => response.json())
    .then(data => data.in_wishlist);
}

function loadWishlistForProduct(productId) {
  const span = document.getElementById(`wishlist-${productId}`);
  if (!span) return;
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
}

window.onload = function() {
  const productId = document.getElementById('product_id').value;
  loadWishlistForProduct(productId);
};
