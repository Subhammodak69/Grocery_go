async function poster_create() {
    const messageEl = document.getElementById('message');
    messageEl.textContent = '';
    messageEl.className = 'message';

    const product_id = document.getElementById('product_id').value.trim();
    const title = document.getElementById('title').value.trim();
    const description = document.getElementById('description').value.trim();
    const fileInput = document.getElementById('image');
    const file = fileInput.files[0];
    const start_date = document.getElementById('start_date').value.trim();
    const end_date = document.getElementById('end_date').value.trim();

    console.log("product id is =>"+product_id);
    if (!product_id || !title || !description || !file || !start_date || !end_date) {
        messageEl.textContent = 'Please fill all required fields.';
        messageEl.classList.add('error');
        return;
    }

    const formData = new FormData();
    formData.append('product_id', product_id);
    formData.append('title', title);
    formData.append('description', description);
    formData.append('image', file); // append the actual file here
    formData.append('start_date', start_date);
    formData.append('end_date', end_date);

    try {
        const response = await fetch('/admin/poster/create/', {
            method: 'POST',
            credentials: 'include',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to create poster.');
        }

        messageEl.textContent = 'Poster created successfully! Redirecting.....';
        messageEl.classList.add('success');
        document.getElementById('adminposterForm').reset();
        document.getElementById('preview').innerHTML = '';

        // Redirect after success
        setTimeout(() => {
            window.location.href = '/admin/posters/';
        }, 1000);
    } catch (err) {
        messageEl.textContent = err.message;
        messageEl.classList.add('error');
    }
}
