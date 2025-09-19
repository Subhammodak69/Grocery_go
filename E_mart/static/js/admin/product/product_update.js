async function product_update() {
    const messageEl = document.getElementById('message');
    messageEl.textContent = '';
    messageEl.className = 'message';
    
    const productId = document.getElementById('product_id').value;
    const category_id = document.getElementById('category').value;
    const name = document.getElementById('name').value.trim();
    const description = document.getElementById('description').value.trim();
    const price = document.getElementById('price').value.trim();
    const stock = document.getElementById('stock').value.trim();
    const size = document.getElementById('size').value.trim();

    if (!category_id || !name || !description || !file || !price || !stock || !size) {
        messageEl.textContent = 'Please fill all required fields.';
        messageEl.classList.add('error');
        return;
    }

    const formData = new FormData();
    formData.append('category_id',category_id);
    formData.append('name', name);
    formData.append('description', description);
    formData.append('price', price);
    formData.append('stock', stock);
    formData.append('size', size);
    if (file !== undefined) {
        formData.append('image', file);
    }

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

