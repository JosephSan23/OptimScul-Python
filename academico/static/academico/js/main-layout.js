document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const btnToggle = document.getElementById('btn-toggle');
    const hasSubmenu = document.querySelectorAll('.has-submenu');
    const userTrigger = document.getElementById('user-menu-trigger');
    const userDropdown =  document.getElementById('user-dropdown');
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-item a');

    navLinks.forEach(link => {
        const targetPath = link.getAttribute('data-path');
        
        // Si la ruta actual empieza con el path del link (ej: /usuarios/editar coincide con /usuarios)
        if (currentPath.startsWith(targetPath)) {
            link.parentElement.classList.add('active');
        }
    });

    // boton hamburguesa
    if (btnToggle && sidebar) {
        btnToggle.addEventListener('click', (e) => {
            e.preventDefault();
            sidebar.classList.toggle('collapsed');

            if (sidebar.classList.contains('collapsed')) {
                hasSubmenu.forEach(item => item.classList.remove('open'));
            }

            console.log('Sidebar colapsado: ', sidebar.classList.contains('collapsed'));
        });
    }

    // submenus
    hasSubmenu.forEach(item => {
        const header = item.querySelector('.submenu-header');
        if (header) {
            header.addEventListener('click', (e) => {
                if (sidebar.classList.contains('collapsed')) return;

                e.preventDefault();
                e.stopPropagation();

                // cerrar otros menus abiertos
                hasSubmenu.forEach(otherItem => {
                    if (otherItem !== item) otherItem.classList.remove('open');
                });

                item.classList.toggle('open');  
            });
        }
    });

    if (userTrigger && userDropdown) {
        userTrigger.addEventListener('click', (e) => {
            e.stopPropagation();
            userDropdown.classList.toggle('active');
        });

        document.addEventListener('click', () => {
            userDropdown.classList.remove('active');
        });
    }
});