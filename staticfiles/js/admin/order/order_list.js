window.isactive_toggle = function(){
    document.querySelectorAll('.toggle-active').forEach(function(toggle) {
        toggle.addEventListener('change', function() {
            const orderId = this.dataset.orderId;
            const isActive = this.checked;
            console.log('Order toggle:', orderId, isActive);

            fetch(`/admin/orders/toggle-active/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ order_id: orderId, is_active: isActive })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (!data.success) {
                    alert('Failed to update order status.');
                    this.checked = !isActive;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error updating order status.');
                this.checked = !isActive;
            });
        });
    });
}

function create_order(){
    window.location.href='/admin/orders/create/';
}

function update_order(orderId){
    window.location.href=`/admin/orders/update/${orderId}/`;
}
