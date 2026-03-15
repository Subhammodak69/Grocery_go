document.addEventListener('DOMContentLoaded', () => {
    const loader = document.getElementById('loaderdiv');
    window.logout = function(){
        loader.style.display = 'block ';
        fetch('/logout/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken':'csrftoken'
            }
        })
        .finally(() => {
            setTimeout(() => {
                loader.style.display = 'none ';
                window.location.href = '/';
            }, 2000);
        });
    }
})