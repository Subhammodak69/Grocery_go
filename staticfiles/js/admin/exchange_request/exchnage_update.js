async function exchange_update() {
    const messageEl = document.getElementById('message');
    messageEl.textContent = '';
    messageEl.className = 'message';
    
    const exchangeId = document.getElementById('exchange_id').value;
    const order = document.getElementById('order').value.trim();
    const order_item = document.getElementById('order_item').value.trim();
    const user = document.getElementById('user').value.trim();
    const product = document.getElementById('product').value.trim();
    const reason = document.getElementById('reason').value.trim();
    const status = document.getElementById('status').value.trim();
    const purpose = document.getElementById('purpose').value.trim();
    const is_active = document.getElementById('is_active').checked;

    if (!order || !order_item || !user || !product || !reason || !status || !purpose) {
        messageEl.textContent = 'Please fill all required fields.';
        messageEl.classList.add('error');
        return;
    }

    const formData = new FormData();
    formData.append('order', order);
    formData.append('order_item', order_item);
    formData.append('user', user);
    formData.append('product', product);
    formData.append('reason', reason);
    formData.append('status', status);
    formData.append('purpose', purpose);
    formData.append('is_active', is_active);

    try {
        const response = await fetch(`/admin/exchange-requests/update/${exchangeId}/`, {
            method: 'POST',
            credentials: 'include',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to update exchange request.');
        }

        messageEl.textContent = 'Exchange request updated successfully! Redirecting.....';
        messageEl.classList.add('success');

        setTimeout(() => {
            window.location.href = '/admin/exchange-requests/';
        }, 1000);
    } catch (err) {
        messageEl.textContent = err.message;
        messageEl.classList.add('error');
    }
}
