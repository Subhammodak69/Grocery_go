// Attach event listener to form submission
document.getElementById('order-summary-form').addEventListener('submit', handlePlaceOrder);

// Handle place order submission
function handlePlaceOrder(e) {
    e.preventDefault();
    
    const addressField = document.getElementById('delivery-address');
    const address = addressField.value.trim();
    
    // Validation
    if (!address) {
    alert('Please enter a delivery address');
    addressField.focus();
    return;
    }
    
    if (address.length < 10) {
    alert('Please enter a complete delivery address');
    addressField.focus();
    return;
    }
    
    const placeOrderBtn = document.getElementById('placeOrderBtn');
    const btnContent = placeOrderBtn.querySelector('.btn-content');
    const btnLoader = placeOrderBtn.querySelector('.btn-loader');
    
    btnContent.style.display = 'none';
    btnLoader.style.display = 'block';
    placeOrderBtn.disabled = true;
    
    console.log('Sending POST request with address:', address);
    
    // Send fetch request with CSRF token
    fetch('/order/create/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    credentials: 'same-origin',  // Include cookies
    body: JSON.stringify({
        address: address
    })
    })
    .then(response => {
    console.log('Response status:', response.status);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
    })
    .then(data => {
    console.log('Response data:', data);
    
    if (data.success) {
        alert('Order placed successfully!');
        window.location.href = data.redirect_url || '/orders/';
    } else {
        alert('Failed to place order: ' + (data.message || 'Unknown error'));
        btnContent.style.display = 'block';
        btnLoader.style.display = 'none';
        placeOrderBtn.disabled = false;
    }
    })
    .catch(error => {
    console.error('Error:', error);
    alert('Error placing order. Please try again.');
    btnContent.style.display = 'block';
    btnLoader.style.display = 'none';
    placeOrderBtn.disabled = false;
    });
}

// Attach click handler to place order button
document.getElementById('placeOrderBtn').addEventListener('click', function(e) {
    // Form submission is handled by the form's submit event
});
