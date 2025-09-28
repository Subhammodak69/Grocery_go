async function product_details_create() {
    const messageEl = document.getElementById('message');
    messageEl.textContent = '';
    messageEl.className = ''; 

    // Get form field values
    const productId = document.getElementById('product').value; 
    const price = document.getElementById('price').value.trim();
    const stock = document.getElementById('stock').value.trim();
    const size = document.getElementById('size').value.trim();
    const fileInput = document.getElementById('image');
    const file = fileInput.files[0];
    const isActive = document.getElementById('is_active').checked;

    // Validate required fields
    if (!productId || !price || !stock || !size || !file) {
        messageEl.textContent = 'Please fill all required fields.';
        messageEl.classList.add('error');
        return;
    }

    // Create FormData object for file upload
    const formData = new FormData();
    formData.append('product', productId);
    formData.append('price', price);
    formData.append('stock', stock);
    formData.append('size', size);
    formData.append('image', file);  
    formData.append('is_active', isActive);

    try {
        const response = await fetch('/admin/product_details/create/', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'X-CSRFToken':'csrftoken'
               
            },
            body: formData 
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to create product details.');
        }

        messageEl.textContent = 'Product details created successfully! Redirecting...';
        messageEl.classList.add('success');
        document.getElementById('adminproduct_detailsForm').reset();
        document.getElementById('preview').innerHTML = '';

        setTimeout(() => {
            window.location.href = '/admin/product_details_lists/';
        }, 1000);
    } catch (err) {
        messageEl.textContent = err.message;
        messageEl.classList.add('error');
    }
}