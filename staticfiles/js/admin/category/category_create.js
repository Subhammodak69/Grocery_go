async function category_create() {
    const messageEl = document.getElementById('message');
    messageEl.textContent = '';
    messageEl.className = 'message';

    const name = document.getElementById('name').value.trim();
    const description = document.getElementById('description').value.trim();
    const fileInput = document.getElementById('image');
    const file = fileInput.files[0];

    if (!name || !description || !file) {
        messageEl.textContent = 'Please fill all required fields.';
        messageEl.classList.add('error');
        return;
    }

    const formData = new FormData();
    formData.append('name', name);
    formData.append('description', description);
    formData.append('image', file); // append the actual file here


    try {
        const response = await fetch('/admin/category/create/', {
            method: 'POST',
            credentials: 'include',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to create category.');
        }

        messageEl.textContent = 'Category created successfully! Redirecting.....';
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
