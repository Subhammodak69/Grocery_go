async function product_create() {
    const messageEl = document.getElementById('message');
    messageEl.textContent = '';
    messageEl.className = 'message';

    const category_id = document.getElementById('category').value;
    const name = document.getElementById('name').value.trim();
    const size = document.getElementById('size').value.trim();
    const price = document.getElementById('price').value.trim();
    const stock = document.getElementById('stock').value.trim();
    const description = document.getElementById('description').value.trim();
    
    const fileInput = document.getElementById('image');
    const file = fileInput.files[0];


    if (!category_id || !name || !size || !price || !stock || !description || !file ) {
        messageEl.textContent = 'Please fill all required fields.';
        messageEl.classList.add('error');
        return;
    }

    const formData = new FormData();
    formData.append('category_id',category_id);
    formData.append('name', name);
    formData.append('size', size);
    formData.append('price', price);
    formData.append('stock', stock);
    formData.append('description', description);
    formData.append('image', file); 

    try {
        const response = await fetch('/admin/product/create/', {
            method: 'POST',
            credentials: 'include',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to create product.');
        }

        messageEl.textContent = 'product created successfully! Redirecting.....';
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
