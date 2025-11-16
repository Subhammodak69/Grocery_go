window.isactive_toggle = function(){
    document.querySelectorAll('.toggle-active').forEach(function(toggle) {
        toggle.addEventListener('change', function() {
            const workerId = this.dataset.workerId;
            const isActive = this.checked;
            console.log(isActive);

            fetch(`/admin/delivery-workers/toggle-active/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ worker_id: workerId, is_active: isActive })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (!data.success) {
                    alert('Failed to update worker status.');
                    this.checked = !isActive;
                }
            })
            .catch(error => {
                alert('Error updating worker status.');
                this.checked = !isActive;
            });
        });
    });
}

function create_worker(){
    window.location.href='/admin/delivery-worker/create/';
}

function update_worker(workerId){
    window.location.href=`/admin/delivery-worker/update/${workerId}`;
}