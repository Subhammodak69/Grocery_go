window.isactive_toggle = function(){
    document.querySelectorAll('.toggle-active').forEach(function(toggle) {
        toggle.addEventListener('change', function() {
            const deliveryId = this.dataset.deliveryId;
            const isActive = this.checked;
            console.log('Delivery toggle:', deliveryId, isActive);

            fetch(`/admin/delivery/toggle-active/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ delivery_id: deliveryId, is_active: isActive })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (!data.success) {
                    alert('Failed to update delivery status.');
                    this.checked = !isActive;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error updating delivery status.');
                this.checked = !isActive;
            });
        });
    });
}

function create_delivery(){
    window.location.href='/admin/deliveries-or-pickups/create/';
}

function update_delivery(deliveryId){
    window.location.href=`/admin/deliveries-or-pickups/update/${deliveryId}/`;
}
