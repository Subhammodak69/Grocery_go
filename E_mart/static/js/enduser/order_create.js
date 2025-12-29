function create_order(){
    console.log("called...............");
    const addressField = document.getElementById('delivery-address');
    const address = addressField ? addressField.value.trim() : '';
    const final_price = document.getElementById('final_price').value;
    const delivery_fee = document.getElementById('delivery_fee').value;
    const discount = document.getElementById('discount').value;

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

    fetch('/order/create/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({
            address: address,
            final_price: final_price,
            delivery_fee: delivery_fee,
            discount: discount
        })
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        console.log(JSON.stringify(data));
        if (data.success) {
            showMessage(
                'success',
                'Order Placed Successfully! Redirecting...'
            );
            setTimeout(() => {
                window.location.href = `/order/${data.order_id}/`;
                },1000);
        } else {
            showMessage('error', data.message);
            setTimeout(() => {
                window.location.href = `/user/cart/`;
            },1000);
            
        }
    })
    .catch(error => {
        showMessage('error', error.message || error);
        setTimeout(() => {
        window.location.href = `/user/cart/`;
        },1000);
    });
}
