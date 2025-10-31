// admin_Workercreate.js

async function Worker_create() {
    const messageEl = document.getElementById('message');
    messageEl.textContent = '';
    messageEl.className = 'message';

    const first_name = document.getElementById('first_name').value.trim();
    const last_name = document.getElementById('last_name').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone_number = document.getElementById('phone_number').value.trim();
    const address = document.getElementById('address').value.trim();

    // Validate required fields (address may be optional based on your backend validation)
    if (!first_name || !last_name || !email || !phone_number || !address) {
        messageEl.textContent = 'Please fill all required fields.';
        messageEl.classList.add('error');
        return;
    }
    document.getElementById('adminWorkerForm').reset()
    try {
        const response = await fetch('/admin/delivery-worker/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include', // if your session or auth needs it
            body: JSON.stringify({
                first_name,
                last_name,
                email,
                phone_number,
                address
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to create Worker.');
        }

        messageEl.textContent = 'Worker created successfully! Redirecting.....';
        messageEl.classList.add('success');

        // Optionally redirect after success
        setTimeout(()=>{
            window.location.href = '/admin/workers/';
        },1000);
    } catch (err) {
        messageEl.textContent = err.message;
        messageEl.classList.add('error');
    }
}
