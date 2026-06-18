from django.urls import path
from . import views

app_name = 'academico'

urlpatterns = [
    # Pantallas principales
    path('mis-cursos/', views.ListaCursosView.as_view(), name='lista_cursos'),
    path('mis-cursos/<int:curso_id>/materias/', views.ListaMateriasCursoView.as_view(), name='lista_materias_curso'),
    path('mis-cursos/<int:curso_id>/materias/<int:asignatura_id>/panel/', views.PanelMateriaView.as_view(), name='panel_materia'),
    path('mis-cursos/<int:curso_id>/materias/<int:asignatura_id>/actividades/crear/', 
     views.CrearActividadView.as_view(), 
     name='crear_actividad'),
]