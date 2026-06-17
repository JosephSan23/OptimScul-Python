function abrirModal(id) {
        document.getElementById(id).showModal();
    }

    function cerrarModal(id) {
        document.getElementById(id).close();
    }

    function irAPanel(idCurso, idAsignatura) {
        console.log(`Redirigiendo al Panel del curso ${idCurso} y materia ${idAsignatura}`);

        window.location.href = `/academico/mis-cursos/${idCurso}/materias/${idAsignatura}/panel/`;
    }

    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.close();
        });
    });