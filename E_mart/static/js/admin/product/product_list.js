window.isactive_toggle = function(){
    document.querySelectorAll('.toggle-active').forEach(function(toggle) {
        toggle.addEventListener('change', function() {
            const productId = this.dataset.productId;
            const isActive = this.checked;
            console.log(isActive);

            fetch(`/admin/products/toggle-active/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ product_id: productId, is_active: isActive })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (!data.success) {
                    alert('Failed to update product status.');
                    this.checked = !isActive;
                }
            })
            .catch(error => {
                alert('Error updating product status.');
                this.checked = !isActive;
            });
        });
    });
}

function create_product(){
    window.location.href='/admin/product/create/';
}

function update_product(productId){
    window.location.href=`/admin/product/update/${productId}`;
}