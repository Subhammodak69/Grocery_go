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


// Open review modal function
window.openreviewmodal = function() {
    document.getElementById('reviewModal').style.display = 'block';
  }

  // Star rating toggle & sum logic
  const stars = document.querySelectorAll('#starRating .star');
  const ratingInput = document.getElementById('rating');

  stars.forEach(star => {
    star.addEventListener('click', () => {
      star.classList.toggle('selected');
      updateRating();
    });
  });

function updateRating() {
    let total = 0;
    stars.forEach(star => {
      if (star.classList.contains('selected')) {
        total += parseInt(star.getAttribute('data-value'));
      }
    });
    ratingInput.value = total;
    console.log('Current total rating:', total);
  }

  // Photo upload & preview
  const photoIcon = document.getElementById('photoIcon');
  const photoInput = document.getElementById('photoInput');
  const photoPreviewContainer = document.getElementById('photoPreviewContainer');
  const photoPreview = document.getElementById('photoPreview');

  photoIcon.addEventListener('click', () => {
    photoInput.click();
  });

  photoInput.addEventListener('change', () => {
    const file = photoInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = e => {
        photoPreview.src = e.target.result;
        photoPreviewContainer.style.display = 'block';
      };
      reader.readAsDataURL(file);
    } else {
      photoPreview.src = '';
      photoPreviewContainer.style.display = 'none';
    }
  });

  

  // Submit review via AJAX with photo base64
function create_review() {
    const product_id = document.getElementById('product_id').value;
    const rating = document.getElementById('rating').value;
    const review = document.getElementById('review').value;

    if (photoInput.files.length > 0) {
      const file = photoInput.files[0];
      const reader = new FileReader();
      reader.onload = function(e) {
        const photo_url = e.target.result;
        sendReviewData(product_id, photo_url, rating, review);
      };
      reader.readAsDataURL(file);
    } else {
      console.log("not selected");
      sendReviewData(product_id, '', rating, review);
    }
  }

function sendReviewData(product_id, photo_url, rating, review) {
  fetch('/review/create/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      product_id: product_id,
      photo_url: photo_url,
      rating: rating,
      review: review,
    }),
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      console.log('Review submitted successfully!');
      console.log(data.data);

      // Reset form fields FIRST
      const reviewForm = document.getElementById('reviewForm');
      if (reviewForm) reviewForm.reset();
      
      const ratingField = document.getElementById('rating');
      if (ratingField) ratingField.value = '';
      
      const photoPreview = document.getElementById('photoPreview');
      if (photoPreview) photoPreview.src = '';
      
      const photoPreviewContainer = document.getElementById('photoPreviewContainer');
      if (photoPreviewContainer) photoPreviewContainer.style.display = 'none';

      // Close the review modal
      const reviewModal = document.getElementById('reviewModal');
      if (reviewModal) reviewModal.style.display = 'none';

      // Extract data from response
      const reviewData = data.data;
      const createdByFullname = reviewData.created_by_fullname || 'Anonymous';
      const createdAt = new Date(reviewData.created_at).toLocaleString('en-US', {
        month: 'short', 
        day: '2-digit', 
        year: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit'
      });
      const reviewText = reviewData.review;
      const photoUrl = reviewData.photo;

      // Generate stars using rating_range and empty_range arrays from backend
      let starsHtml = '';
      
      // Add filled stars
      if (Array.isArray(reviewData.rating_range)) {
        reviewData.rating_range.forEach(() => {
          starsHtml += '⭐';
        });
      }

      // Add empty stars
      if (Array.isArray(reviewData.empty_range)) {
        reviewData.empty_range.forEach(() => {
          starsHtml += '☆';
        });
      }

      // Create new review element
      const reviewsContainer = document.getElementById('reviews-show');
      
      if (reviewsContainer) {
        const newReviewDiv = document.createElement('div');
        newReviewDiv.innerHTML = `
          <div>
            <div class="d-flex justify-content-between items-center">
              <div class="d-flex gap-2 font-bold">
                <p style="font-weight: bold; margin:0px!important;">${createdByFullname}</p>
                <div>${createdAt}</div>
              </div>
              <div>${starsHtml}</div>
            </div>
            <p class="text-gray-700 mb-2 m-auto" style="width:96%;">${reviewText}</p>
            ${photoUrl ? `<img src="${photoUrl}" alt="Review photo" class="max-w-xs rounded-md mb-2 shadow" />` : ''}
          </div>
        `;

        // Insert at the top of reviews container
        reviewsContainer.insertBefore(newReviewDiv, reviewsContainer.firstChild);
        
        console.log('Review added to DOM successfully');
      } else {
        console.error('Reviews container not found');
      }

    } else {
      alert('Error: ' + (data.error || 'Unknown error'));
    }
  })
  .catch(error => {
    console.error('Fetch error:', error);
    alert('Fetch error: ' + error);
  });
}
