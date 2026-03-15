async function category_update() {
    const messageEl = document.getElementById('message');
    messageEl.textContent = '';
    messageEl.className = 'message';
    const categoryId = document.getElementById('category_id').value;
    const name = document.getElementById('name').value.trim();
    const description = document.getElementById('description').value.trim();
    const fileInput = document.getElementById('image');
    const file = fileInput.files[0];

    if (!name || !description ) {
        messageEl.textContent = 'Please fill all required fields.';
        messageEl.classList.add('error');
        return;
    }

    const formData = new FormData();
    formData.append('name', name);
    formData.append('description', description);
    if (file !== undefined) {
        formData.append('image', file);
    }

    try {
        const response = await fetch(`/admin/category/update/${categoryId}/`, {
            method: 'POST',
            credentials: 'include',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to update category.');
        }

        messageEl.textContent = 'Category updated successfully! Redirecting.....';
        messageEl.classList.add('success');
        document.getElementById('admincategoryForm').reset();
        document.getElementById('preview').innerHTML = '';

        // Redirect after success
        setTimeout(() => {
            window.location.href = '/admin/categories/';
        }, 1000);
    } catch (err) {
        messageEl.textContent = err.message;
        messageEl.classList.add('error');
    }
}

