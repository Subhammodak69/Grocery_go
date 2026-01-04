window.addEventListener('load', function() {
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.tab a');
    
    navItems.forEach(function(link) {
        link.classList.remove('active');
        if (currentPath === new URL(link.href).pathname) {
            console.log(currentPath);
            console.log(link.href.pathname);
            link.classList.add('active');
            const tabContainer = link.closest('.tab');
            if (tabContainer) {
                tabContainer.style.background = '#0c0c0c35';
                tabContainer.style.borderRadius = '10px';
                tabContainer.style.padding = '0px 10px';
            }
        }
    });
});
