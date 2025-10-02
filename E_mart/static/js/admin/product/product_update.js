async function product_update() {
    const messageEl = document.getElementById('message');
    messageEl.textContent = '';
    messageEl.className = 'message';
    
    const productId = document.getElementById('product_id').value;
    const category_id = document.getElementById('category').value;
    const name = document.getElementById('name').value.trim();
    const description = document.getElementById('description').value.trim();
    

    if (!category_id || !name || !description) {
        messageEl.textContent = 'Please fill all required fields.';
        messageEl.classList.add('error');
        return;
    }

    const formData = new FormData();
    formData.append('category_id',category_id);
    formData.append('name', name);
    formData.append('description', description);

    try {
        const response = await fetch(`/admin/product/update/${productId}/`, {
            method: 'POST',
            credentials: 'include',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to update product.');
        }

        messageEl.textContent = 'product updated successfully! Redirecting.....';
        messageEl.classList.add('success');
        document.getElementById('adminproductForm').reset();
        document.getElementById('preview').innerHTML = '';

        // Redirect after success
        setTimeout(() => {
            window.location.href = '/admin/products/';
        }, 1000);
    } catch (err) {
        messageEl.textContent = err.message;
        messageEl.classList.add('error');
    }
}

