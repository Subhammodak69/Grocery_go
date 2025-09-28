function initToggleActive() {
    document.querySelectorAll('.toggle-active').forEach(function(toggle) {
        toggle.addEventListener('change', function() {
            const productDetailsId = this.dataset.productDetailId;
            const isActive = this.checked;
            
            fetch(`/admin/product_details/toggle-active/`, { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': 'csrfToken'
                },
                credentials: 'include',
                body: JSON.stringify({ 
                    product_details_id: productDetailsId, 
                    is_active: isActive 
                }) 
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (!data.success) {
                    alert('Failed to update product details status.');
                    this.checked = !isActive; // Revert toggle state
                }
            })
            .catch(error => {
                console.error('Error:', error);
                this.checked = !isActive; // Revert toggle state
            });
        });
    });
}

document.addEventListener('DOMContentLoaded', initToggleActive);
window.initToggleActive = initToggleActive;


function create_product_details() {
    window.location.href = '/admin/product_details/create/';
}

function update_product_details(productDetailsId) {
    window.location.href = `/admin/product_details/update/${productDetailsId}/`;
}
