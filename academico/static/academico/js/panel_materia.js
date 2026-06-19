let modoEdicion = false;
let actividadEditandoId = null;
let cardEditando = null;

function cambiarTab(tabEl, seccionId) {
    document.querySelectorAll('.tab').forEach(t => {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
    });
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));

    tabEl.classList.add('active');
    tabEl.setAttribute('aria-selected', 'true');
    
    const seccion = document.getElementById(seccionId);
    if (seccion) {
        seccion.classList.add('active');
    }
}

function publicarAviso() {
    const input = document.getElementById('anuncio-input');
    if (!input) return;
    
    const texto = input.value.trim();
    if (!texto) return;

    const lista = document.getElementById('aviso-list');
    const card = document.createElement('div');
    card.className = 'aviso-card';
    card.innerHTML = `
        <div class="aviso-avatar">U</div>
        <div>
            <span class="aviso-author">Usuario Activo
                <span class="aviso-date">ahora mismo</span>
            </span>
            <p class="aviso-text">${texto}</p>
        </div>`;
    
    if (lista.firstChild) {
        lista.insertBefore(card, lista.firstChild);
    } else {
        lista.appendChild(card);
    }
    input.value = '';
}

function verEntregas(idActividad) {
    const tabCalif = document.querySelector('[aria-controls="sec-calificaciones"]');
    if (tabCalif) {
        cambiarTab(tabCalif, 'sec-calificaciones');
        
        console.log(`Abriendo matriz de notas para la actividad ID: ${idActividad}`);
    }
}

function abrirModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.showModal();
}

function cerrarModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.close();
}

function guardarActividad() {
    const nombre = document.getElementById('act-nombre').value.trim();
    const descripcion = document.getElementById('act-descripcion').value.trim();
    const fecha = document.getElementById('act-fecha').value;

    if (!nombre) { alert('El nombre de la actividad es obligatorio.'); return; }

    const urlParts = window.location.pathname.split('/');
    const cursoId = urlParts[3];
    const asignaturaId = urlParts[5];

    const url = modoEdicion
        ? `/academico/mis-cursos/${cursoId}/materias/${asignaturaId}/actividades/${actividadEditandoId}/editar/`
        : `/academico/mis-cursos/${cursoId}/materias/${asignaturaId}/actividades/crear/`;

    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre, descripcion, fecha_limite: fecha || null })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.ok) { alert('Error: ' + data.error); return; }

        const fechaTexto = data.fecha_limite
            ? new Date(data.fecha_limite + 'T00:00:00').toLocaleDateString('es-CO', { day: 'numeric', month: 'short', year: 'numeric' })
            : 'Sin fecha límite';

        if (modoEdicion && cardEditando) {
            // Actualiza la card existente en el DOM
            cardEditando.querySelector('.actividad-name').textContent = data.nombre;
            cardEditando.querySelector('.actividad-meta').innerHTML = `<i class="ti ti-calendar"></i> Vence ${fechaTexto}`;
            // Actualiza los data attributes del botón editar
            const btnEditar = cardEditando.querySelector('[onclick="editarActividad(this)"]');
            if (btnEditar) {
                btnEditar.dataset.nombre = data.nombre;
                btnEditar.dataset.descripcion = descripcion;
                btnEditar.dataset.fecha = data.fecha_limite ?? '';
            }
            const btnEliminar = cardEditando.querySelector('[onclick="eliminarActividad(this)"]');
            if (btnEliminar) {
                btnEliminar.dataset.nombre = data.nombre;
            }
        } else {
            // Crea nueva card
            const lista = document.getElementById('actividades-list');
            const card = document.createElement('div');
            card.className = 'actividad-card';
            card.innerHTML = `
                <div class="actividad-left">
                    <div class="actividad-icon"><i class="ti ti-file-text" aria-hidden="true"></i></div>
                    <div>
                        <div class="actividad-name">${data.nombre}</div>
                        <div class="actividad-meta">
                            <i class="ti ti-calendar" aria-hidden="true"></i> Vence ${fechaTexto}
                        </div>
                    </div>
                </div>
                <div class="actividad-right">
                    <span class="pill green">0 / -- entregaron</span>
                    <button class="btn btn--ghost" type="button" onclick="verEntregas('${data.id}')">Ver entregas</button>
                    <button class="btn btn--ghost btn--icon" type="button"
                        data-id="${data.id}"
                        data-nombre="${data.nombre}"
                        data-descripcion="${descripcion}"
                        data-fecha="${data.fecha_limite ?? ''}"
                        onclick="editarActividad(this)">
                        <i class="ti ti-pencil"></i>
                    </button>
                    <button class="btn btn--ghost btn--icon" type="button"
                        data-id="${data.id}"
                        data-nombre="${data.nombre}"
                        onclick="eliminarActividad(this)">
                        <i class="ti ti-trash"></i>
                    </button>
                </div>`;
            lista.appendChild(card);
        }

        cerrarModal('modal-actividad');
    })
    .catch(err => alert('Error de conexión: ' + err));
}

function filtrarAlumnos(query) {
    const q = query.toLowerCase();
    const filas = document.querySelectorAll('#alumnos-tbody tr');
    let visibles = 0;
    
    filas.forEach(fila => {
        if (!fila.dataset.nombre) return; 
        
        const nombre = fila.dataset.nombre.toLowerCase();
        const doc    = fila.dataset.doc.toLowerCase();
        const coincide = nombre.includes(q) || doc.includes(q);
        
        fila.style.display = coincide ? '' : 'none';
        if (coincide) visibles++;
    });
    
    const countEl = document.getElementById('alumno-count');
    if (countEl) {
        countEl.textContent = `${visibles} estudiante${visibles !== 1 ? 's' : ''}`;
    }
}

function actualizarNotaRapida(inputEl) {
    const estudianteId = inputEl.dataset.estudiante;
    const actividadId = inputEl.dataset.actividad;
    const nuevaNota = inputEl.value;

    console.log(`Guardando nota de estudiante ${estudianteId} en actividad ${actividadId}: ${nuevaNota}`);
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', e => {
            if (e.target === modal) modal.close();
        });
    });
});

function abrirModalCrear() {
    modoEdicion = false;
    actividadEditandoId = null;
    cardEditando = null;

    document.getElementById('modal-act-title').textContent = 'Nueva actividad';
    document.getElementById('act-nombre').value = '';
    document.getElementById('act-descripcion').value = '';
    document.getElementById('act-fecha').value = '';
    document.getElementById('act-valor').value = '';

    abrirModal('modal-actividad');
}

function editarActividad(btn) {
    modoEdicion = true;
    actividadEditandoId = btn.dataset.id;
    cardEditando = btn.closest('.actividad-card');

    document.getElementById('modal-act-title').textContent = 'Editar actividad';
    document.getElementById('act-nombre').value = btn.dataset.nombre;
    document.getElementById('act-descripcion').value = btn.dataset.descripcion;
    document.getElementById('act-fecha').value = btn.dataset.fecha;

    abrirModal('modal-actividad');
}

function eliminarActividad(btn) {
    const id = btn.dataset.id;
    const nombre = btn.dataset.nombre;
    const card = btn.closest('.actividad-card');

    document.getElementById('nombre-actividad-eliminar').textContent = `"${nombre}"`;

    const btnConfirmar = document.getElementById('btn-confirmar-eliminar');
    // Clonar para limpiar listeners anteriores
    const btnNuevo = btnConfirmar.cloneNode(true);
    btnConfirmar.parentNode.replaceChild(btnNuevo, btnConfirmar);

    btnNuevo.addEventListener('click', () => {
        const urlParts = window.location.pathname.split('/');
        const cursoId = urlParts[3];
        const asignaturaId = urlParts[5];

        fetch(`/academico/mis-cursos/${cursoId}/materias/${asignaturaId}/actividades/${id}/eliminar/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(res => res.json())
        .then(data => {
            if (!data.ok) { alert('Error: ' + data.error); return; }
            card.remove();
            cerrarModal('modal-confirmar-eliminar');
        })
        .catch(err => alert('Error de conexión: ' + err));
    });

    abrirModal('modal-confirmar-eliminar');
}