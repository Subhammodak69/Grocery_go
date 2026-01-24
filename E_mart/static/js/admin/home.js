document.addEventListener('DOMContentLoaded', function(){
    function updateBadges() {
        fetch('/api/admin/notifications/')
        .then(res => res.json())
        .then(data => {
            // Update Orders badge
            let ordersBadge = document.querySelector('[href="/admin/unassigned/orders/"] .badge');
            if (data.unassigned_orders_count > 0) {
                if (!ordersBadge) {
                    ordersBadge = document.createElement('span');
                    ordersBadge.className = 'badge bg-danger position-absolute translate-middle';
                    ordersBadge.style.right = '10%';
                    ordersBadge.style.top = '50%';
                    ordersBadge.style.borderRadius = '50%';
                    document.querySelector('[href="/admin/unassigned/orders/"]').appendChild(ordersBadge);
                }
                ordersBadge.textContent = data.unassigned_orders_count;
            } else if (ordersBadge) {
                ordersBadge.remove();
            }

            // Update Pickups badge
            let pickupsBadge = document.querySelector('[href="/admin/unassigned/pickups/"] .badge');
            if (data.unassigned_pickups_count > 0) {
                if (!pickupsBadge) {
                    pickupsBadge = document.createElement('span');
                    pickupsBadge.className = 'badge bg-danger position-absolute translate-middle';
                    pickupsBadge.style.right = '10%';
                    pickupsBadge.style.top = '50%';
                    pickupsBadge.style.borderRadius = '50%';
                    document.querySelector('[href="/admin/unassigned/pickups/"]').appendChild(pickupsBadge);
                }
                pickupsBadge.textContent = data.unassigned_pickups_count;
            } else if (pickupsBadge) {
                pickupsBadge.remove();
            }
        });
    }

    // Load initially
    updateBadges();
    
    // Update every 15 seconds
    setInterval(updateBadges, 15000);
});
