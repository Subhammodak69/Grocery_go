document.addEventListener('DOMContentLoaded', function() {
    let modal = document.getElementById('remove-modal');
    let modalRemoveBtn = document.getElementById('modal-remove-btn');
    let modalCancelBtn = document.getElementById('modal-cancel-btn');
    let itemToRemove = null;

    // Open modal on delete click
    document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', function() {
    const cartItem = btn.closest('.cart-item');
    itemToRemove = cartItem;
    modal.style.display = 'flex';
    });
    });

    // Cancel removes modal
    modalCancelBtn.onclick = function() {
    modal.style.display = 'none';
    itemToRemove = null;
    }

    // Remove: ADD your AJAX logic for backend call here
    modalRemoveBtn.onclick = async function() {
    // Get cartId value (should be a property)
    let cartId = document.getElementById('cartId').value; 
    console.log("cart_id"+cartId);

    if (itemToRemove) {
        try {
        console.log(itemToRemove.dataset.itemId);
        // Send a POST request to remove the item from the cart
        const response = await fetch(`/api/cart/remove-item/${cartId}/`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            // Add auth tokens or CSRF if needed
            },
            body: JSON.stringify({
            itemId: itemToRemove.dataset.itemId // Send the item ID
            })
        });

        if (response.ok) {
            // Remove DOM element only if the backend confirms deletion
            itemToRemove.remove();
            setTimeout(()=>{
                window.location.reload();
            },1000);
        } else {
            // Optionally notify the user of failure
            alert('Failed to remove the item. Please try again.');
        }
        } catch (error) {
        // Handle network or other errors
        alert('Error removing item: ' + error.message);
        }
    }else{
        console.error("not triggered remove btn");
    }

    // Close modal and clear reference
    modal.style.display = 'none';
    itemToRemove = null;
    }


    // Optional: dismiss modal on outside click
    modal.onclick = function(e) {
    if (e.target === modal) {
    modal.style.display = 'none';
    itemToRemove = null;
    }
    }
});