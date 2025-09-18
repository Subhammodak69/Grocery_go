window.isactive_toggle = function(){
    document.querySelectorAll('.toggle-active').forEach(function(toggle) {
        toggle.addEventListener('change', function() {
            const posterId = this.dataset.posterId;
            const isActive = this.checked;
            console.log(isActive);

            fetch(`/admin/posters/toggle-active/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ poster_id: posterId, is_active: isActive })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (!data.success) {
                    alert('Failed to update poster status.');
                    this.checked = !isActive;
                }
            })
            .catch(error => {
                alert('Error updating poster status.');
                this.checked = !isActive;
            });
        });
    });
}

function create_poster(){
    window.location.href='/admin/poster/create/';
}

function update_poster(posterId){
    window.location.href=`/admin/poster/update/${posterId}`;
}