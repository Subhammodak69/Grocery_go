async function product_details_update() {
    const messageEl = document.getElementById('message');
    messageEl.textContent = '';
    messageEl.className = ''; 

    const productDetailsId = document.getElementById('product_details_id').value;
    const productId = document.getElementById('product').value;
    const price = document.getElementById('price').value.trim();
    const stock = document.getElementById('stock').value.trim();
    const size = document.getElementById('size').value.trim();
    const isActive = document.getElementById('is_active').checked;

    const fileInput = document.getElementById('image');
    const file = fileInput.files[0]; 

    // Validate required fields (image not required for update)
    if (!productId || !price || !stock || !size) {
        messageEl.textContent = 'Please fill all required fields.';
        messageEl.classList.add('error');
        return;
    }

    // Use FormData to handle file upload
    const formData = new FormData();
    formData.append('product', productId);
    formData.append('price', price);
    formData.append('stock', stock);
    formData.append('size', size);
    formData.append('is_active', isActive ? 'true' : 'false'); // ✅ Explicit boolean conversion

    // ✅ Only append file if one is actually selected
    if (file) {
        formData.append('image', file);
    }

    // ✅ Add CSRF token to FormData
    const csrfToken = getCookie('csrftoken');
    if (csrfToken) {
        formData.append('csrfmiddlewaretoken', csrfToken);
    }

    try {
        const response = await fetch(`/admin/product_details/update/${productDetailsId}/`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'X-CSRFToken': csrfToken  // ✅ Also add to headers for extra safety
            },
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to update product details.');
        }

        const result = await response.json();
        messageEl.textContent = result.message || 'Product details updated successfully! Redirecting...';
        messageEl.classList.add('success');
        
        // Don't reset form on update - user might want to see current values
        document.getElementById('preview').innerHTML = '';

        setTimeout(() => {
            window.location.href = '/admin/product_details_lists/';
        }, 1000);
    } catch (err) {
        messageEl.textContent = err.message;
        messageEl.classList.add('error');
        console.error('Update error:', err); // ✅ Add console logging for debugging
    }
}