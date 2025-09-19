window.isactive_toggle = function(){
    document.querySelectorAll('.toggle-active').forEach(function(toggle) {
        toggle.addEventListener('change', function() {
            const categoryId = this.dataset.categoryId;
            const isActive = this.checked;
            console.log(isActive);

            fetch(`/admin/categories/toggle-active/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ category_id: categoryId, is_active: isActive })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (!data.success) {
                    alert('Failed to update category status.');
                    this.checked = !isActive;
                }
            })
            .catch(error => {
                alert('Error updating category status.');
                this.checked = !isActive;
            });
        });
    });
}

function create_category(){
    window.location.href='/admin/category/create/';
}

function update_category(categoryId){
    window.location.href=`/admin/category/update/${categoryId}`;
}