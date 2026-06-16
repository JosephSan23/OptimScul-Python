from django.views.generic import ListView, TemplateView
from .models import ProfesorCursoAsignatura, Curso, Asignatura

# Create your views here.
class ListaCursosView(ListView):
    model = ProfesorCursoAsignatura
    template_name = 'academico/lista_cursos.html'  
    context_object_name = 'cursos_asignados'

    def get_queryset(self):
        profesor_id = 1 
        
        asignaciones = ProfesorCursoAsignatura.objects.filter(id_profesor=profesor_id)
        
        # distinct elimina duplicados
        curso_ids = asignaciones.values_list('id_curso', flat=True).distinct()
        return Curso.objects.filter(id_curso__in=curso_ids)

class ListaMateriasCursoView(ListView):
    model = ProfesorCursoAsignatura
    template_name = 'academico/lista_materias.html'
    context_object_name = 'materias_asignadas'
    
    def get_queryset(self):
        profesor_id = 1
        id_del_curso = self.kwargs['curso_id']
        
        asignaciones = ProfesorCursoAsignatura.objects.filter(
            id_profesor = profesor_id,
            id_curso = id_del_curso
        )
        
        asignatura_ids = asignaciones.values_list('id_asignatura', flat=True)
        return Asignatura.objects.filter(id_asignatura__in=asignatura_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cursos'] = Curso.objects.get(pk=self.kwargs['curso_id'])
        return context
        
        
class PanelMateriaView(TemplateView):
    template_name = 'academico/panel_materia.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['curso'] = Curso.objects.get(pk=self.kwargs['curso_id'])
        context['asignatura'] = Asignatura.objects.get(pk=self.kwargs['asignatura_id'])
        
        return context