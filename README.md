# OptimScul

Proyecto desarrollado con Django para la gestión de procesos académicos y administrativos.

## Requisitos

* Python 3.10 o superior
* pip
* Entorno virtual (venv)

## Instalación

1. Clonar el repositorio:

```bash
git clone <url-del-repositorio>
cd optim_scul
```

2. Crear y activar el entorno virtual:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Ejecutar migraciones:

```bash
python manage.py migrate
```

5. Iniciar el servidor:

```bash
python manage.py runserver
```

## Estructura del proyecto

* `manage.py`: Administrador principal del proyecto.
* `apps/`: Módulos o aplicaciones del sistema.
* `templates/`: Plantillas HTML.
* `static/`: Archivos estáticos (CSS, JS, imágenes).
* `media/`: Archivos cargados por los usuarios.

## Autor

Joseph Santiago Olarte Cardona
