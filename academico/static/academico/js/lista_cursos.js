function abrirModal(id) {
        document.getElementById(id).showModal();
    }

    function cerrarModal(id) {
        document.getElementById(id).close();
    }

    function irAPanel(curso, materia) {
        console.log(`Navegar al panel de ${materia} — ${curso}`);
    }

    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.close();
        });
    });