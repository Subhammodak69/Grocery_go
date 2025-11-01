document.addEventListener('DOMContentLoaded', function() {
    const orderForm = document.getElementById('order-summary-form');
    if (orderForm) {
        orderForm.addEventListener('submit', handlePlaceOrder);
    }

    const placeOrderBtn = document.getElementById('placeOrderBtn');
    if (placeOrderBtn) {
        placeOrderBtn.addEventListener('click', function(e) {
            // Form submission handled by 'submit' event
        });
    }
});

function handlePlaceOrder(e) {
    e.preventDefault();

    const addressField = document.getElementById('delivery-address');
    const address = addressField ? addressField.value.trim() : '';
    const final_price =  document.getElementById('final_price').value;
    const delivery_fee =  document.getElementById('delivery_fee').value;
    const discount =  document.getElementById('discount').value;

    console.log(delivery_fee,final_price,discount);

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
    if (!placeOrderBtn) return;
    const btnContent = placeOrderBtn.querySelector('.btn-content');
    const btnLoader = placeOrderBtn.querySelector('.btn-loader');

    btnContent.style.display = 'none';
    btnLoader.style.display = 'block';
    placeOrderBtn.disabled = true;

    fetch('/order/create/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ address: address,final_price: final_price, delivery_fee:delivery_fee,discount:discount })
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
    })
    .then(data => {
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
        alert('Error placing order. Please try again.');
        btnContent.style.display = 'block';
        btnLoader.style.display = 'none';
        placeOrderBtn.disabled = false;
    });
}
