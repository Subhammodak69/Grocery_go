window.isactive_toggle = function(){
    document.querySelectorAll('.toggle-active').forEach(function(toggle) {
        toggle.addEventListener('change', function() {
            const exchangeId = this.dataset.exchangeId;
            const isActive = this.checked;
            console.log('Exchange toggle:', exchangeId, isActive);

            fetch(`/admin/exchange-requests/toggle-active/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ exchange_id: exchangeId, is_active: isActive })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (!data.success) {
                    alert('Failed to update exchange status.');
                    this.checked = !isActive;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error updating exchange status.');
                this.checked = !isActive;
            });
        });
    });
}

function create_exchange(){
    window.location.href='/admin/exchange-requests/create/';
}

function update_exchange(exchangeId){
    window.location.href=`/admin/exchange-requests/update/${exchangeId}/`;
}
