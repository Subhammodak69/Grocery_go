async function delivery_create() {
    const messageEl = document.getElementById('message');
    messageEl.textContent = '';
    messageEl.className = 'message';

    const order = document.getElementById('order').value.trim();
    const address = document.getElementById('address').value.trim();
    const delivery_person = document.getElementById('delivery_person').value.trim();
    const status = document.getElementById('status').value.trim();
    const purpose = document.getElementById('purpose').value.trim();
    const delivered_at = document.getElementById('delivered_at').value.trim();
    const is_active = document.getElementById('is_active').checked;

    console.log("Creating delivery with order:", order);

    if (!order || !address || !status || !purpose) {
        messageEl.textContent = 'Please fill all required fields.';
        messageEl.classList.add('error');
        return;
    }

    const formData = new FormData();
    formData.append('order', order);
    formData.append('address', address);
    formData.append('delivery_person', delivery_person || '');
    formData.append('status', status);
    formData.append('purpose', purpose);
    formData.append('delivered_at', delivered_at);
    formData.append('is_active', is_active);

    try {
        const response = await fetch('/admin/delivery/create/', {
            method: 'POST',
            credentials: 'include',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to create delivery/pickup.');
        }

        messageEl.textContent = 'Delivery/Pickup created successfully! Redirecting...';
        messageEl.classList.add('success');
        document.getElementById('adminDeliveryForm').reset();
        document.getElementById('is_active').checked = true;

        setTimeout(() => {
            window.location.href = '/admin/delivery/';
        }, 1000);
    } catch (err) {
        messageEl.textContent = err.message;
        messageEl.classList.add('error');
    }
}
