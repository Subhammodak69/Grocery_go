async function worker_update() {
    const messageEl = document.getElementById('message');
    messageEl.textContent = '';
    messageEl.className = 'message';

    const first_name = document.getElementById('first_name').value.trim();
    const workerId = document.getElementById('worker_id').value;
    const last_name = document.getElementById('last_name').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone_number = document.getElementById('phone_number').value.trim();

    // Validate required fields (address may be optional based on your backend validation)
    if (!first_name || !last_name || !email || !phone_number) {
        messageEl.textContent = 'Please fill all required fields.';
        messageEl.classList.add('error');
        return;
    }
    try {
        console.log("trying................");
        const response = await fetch(`/admin/delivery-worker/update/${workerId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                first_name,
                last_name,
                email,
                phone_number,
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to update worker.');
        }

        messageEl.textContent = 'Worker Updated successfully! Redirecting.....';
        messageEl.classList.add('success');
        document.getElementById('adminworkerForm').reset();

        // Optionally redirect after success
        setTimeout(()=>{
            window.location.href = '/admin/delivery-workers/';
        },2000);
    } catch (err) {
        messageEl.textContent = err.message;
        messageEl.classList.add('error');
    }
}
