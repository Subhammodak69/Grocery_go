window.isactive_toggle = function(){
    document.querySelectorAll('.toggle-active').forEach(function(toggle) {
        toggle.addEventListener('change', function() {
            const userId = this.dataset.userId;
            const isActive = this.checked;
            console.log(isActive);

            fetch(`/admin/users/toggle-active/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ user_id: userId, is_active: isActive })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (!data.success) {
                    alert('Failed to update user status.');
                    this.checked = !isActive;
                }
            })
            .catch(error => {
                alert('Error updating user status.');
                this.checked = !isActive;
            });
        });
    });
}

function create_user(){
    window.location.href='/admin/user/create/';
}