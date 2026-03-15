document.addEventListener('DOMContentLoaded', function () {
    const qtyInputs = document.querySelectorAll('.product-quantity');
    const checkboxes = document.querySelectorAll('.product-checkbox');

    function calculatePrice() {
        let totalPrice = 0;
        let listingPrice = 0;

        qtyInputs.forEach(input => {
            const productId = input.dataset.productId;
            const qty = parseInt(input.value) || 0;
            const originalPrice = parseFloat(input.dataset.productPrice) || 0;
            const salePrice = parseFloat(input.dataset.productSalePrice) || 0;

            const checkbox = document.querySelector(
                `.product-checkbox[data-product-id="${productId}"]`
            );

            if (checkbox && checkbox.checked && qty > 0) {
                totalPrice += originalPrice * qty;
                listingPrice += salePrice * qty;
            }
        });

        const discount = totalPrice - listingPrice;

        let delivery_fee = 0.00;
        if (listingPrice > 0 && listingPrice < 500) {
            delivery_fee = 40.00;
        }

        document.getElementById('total_price').value = totalPrice.toFixed(2);
        document.getElementById('listing_price').value = listingPrice.toFixed(2);
        document.getElementById('discount').value = discount.toFixed(2);
        document.getElementById('delivery_fee').value = delivery_fee.toFixed(2);
    }

    qtyInputs.forEach(input => {
        input.addEventListener('input', calculatePrice);
    });

    checkboxes.forEach(box => {
        box.addEventListener('change', calculatePrice);
    });

    calculatePrice();
});



function order_create() {
    const user = document.getElementById('user').value;
    const status = document.getElementById('status').value;

    if (!user || !status) {
        showMessage('User and Status are required', 'error');
        return;
    }

    let items = [];

    document.querySelectorAll('.product-quantity').forEach(input => {
        const productId = input.dataset.productId;
        const qty = parseInt(input.value) || 0;
        const checkbox = document.querySelector(
            `.product-checkbox[data-product-id="${productId}"]`
        );

        if (checkbox && checkbox.checked && qty > 0) {
            items.push({
                product_id: productId,
                quantity: qty
            });
        }
    });

    if (items.length === 0) {
        showMessage('Select at least one product', 'error');
        return;
    }

    const payload = {
        user: user,
        status: status,
        total_price: document.getElementById('total_price').value,
        discount: document.getElementById('discount').value,
        delivery_fee: document.getElementById('delivery_fee').value,
        listing_price: document.getElementById('listing_price').value,
        delivery_address: document.getElementById('delivery_address').value,
        is_active: document.getElementById('is_active').checked,
        items: items
    };

    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showMessage('Order created successfully', 'success');
            document.getElementById('adminOrderForm').reset();
            setTimeout(() => {
                window.location.href = '/admin/orders/';
            }, 1000);
        } else {
            showMessage(data.message || 'Something went wrong', 'error');
        }
    })
    .catch(() => {
        showMessage('Server error', 'error');
    });
}

function showMessage(message,type){
    const messageEl = document.getElementById('message');
    messageEl.innerHTML = message;
    if(type == 'success'){
        messageEl.classList.add('success');
    }else{
        messageEl.classList.add('error');
    }
}




