from django.views.generic import ListView, TemplateView
from .models import ProfesorCursoAsignatura, Curso, Asignatura, Estudiante, Aviso, Actividad, Calificacion, EstudianteCurso
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
class ListaCursosView(ListView):
    model = Curso
    template_name = 'academico/lista_cursos.html'  
    context_object_name = 'cursos_asignados'

    def get_queryset(self):
        profesor_id = 21 
        
        # Agregamos select_related para precargar la información de la asignatura adjunta
        asignaciones = ProfesorCursoAsignatura.objects.filter(id_profesor=profesor_id).select_related('id_asignatura')
        # distinct elimina duplicados
        curso_ids = asignaciones.values_list('id_curso', flat=True).distinct()
        
        cursos = Curso.objects.filter(id_curso__in=curso_ids)
        for curso in cursos:
            curso.materias_del_profesor = asignaciones.filter(id_curso=curso.id_curso)
            
        return cursos

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
        
        id_del_curso = self.kwargs['curso_id']
        id_de_la_asignatura = self.kwargs['asignatura_id']
        
        context['curso'] = Curso.objects.get(pk=id_del_curso)
        context['asignatura'] = Asignatura.objects.get(pk=id_de_la_asignatura)
        
        pca = ProfesorCursoAsignatura.objects.filter(
            id_curso=id_del_curso,
            id_asignatura=id_de_la_asignatura
        ).first()
        
        # Pestaña 1: Avisos
        context['publicaciones'] = Aviso.objects.filter(
            curso_id=id_del_curso,       
            asignatura_id=id_de_la_asignatura  
        ).select_related('autor').order_by('-fecha_publicacion')

        # Pestaña 2: Actividades
        if pca:
            context['asignaciones'] = Actividad.objects.filter(id_pca=pca).order_by('-fecha_limite')
        else:
            context['asignaciones'] = Actividad.objects.none()

        # Pestaña 4: Alumnos
        matriculas = EstudianteCurso.objects.filter(
            id_curso=id_del_curso,
            estado='inscrito'
        ).select_related('id_estudiante__id_estudiante')
    
        
        estudiantes = [m.id_estudiante for m in matriculas]
        context['estudiantes'] = estudiantes

        # Pestaña 3: Planilla de Calificaciones (NUEVA LÓGICA)
        if pca:
            calificaciones_qs = Calificacion.objects.filter(id_actividad__id_pca=pca)
        else:
            calificaciones_qs = Calificacion.objects.none()
        
        # Juntamos las notas en un diccionario rápido usando tuplas de (alumno_id, actividad_id)
        notas_dict = {(c.id_estudiante_id, c.id_actividad_id): c.nota for c in calificaciones_qs}

        # Cruzamos los alumnos con sus notas de una vez
        planilla_alumnos = []
        for est in estudiantes:
            filas_actividades = []
            for trab in context['asignaciones']:
                nota_actual = notas_dict.get((est.id_estudiante_id, trab.id_actividad), '')
                filas_actividades.append({
                    'actividad_id': trab.id_actividad,
                    'nota': nota_actual
                })
            planilla_alumnos.append({
                'estudiante': est,
                'actividades': filas_actividades
            })
        
        context['planilla_alumnos'] = planilla_alumnos

        return context
    
    
@method_decorator(csrf_exempt, name='dispatch')
class CrearActividadView(View):
    def post(self, request, curso_id, asignatura_id):
        try:
            data = json.loads(request.body)
            
            pca = ProfesorCursoAsignatura.objects.filter(
                id_curso=curso_id,
                id_asignatura=asignatura_id
            ).first()
            
            if not pca:
                return JsonResponse({'error': 'No se encontró la asignación'}, status=404)
            
            actividad = Actividad.objects.create(
                nombre=data.get('nombre'),
                descripcion=data.get('descripcion', ''),
                fecha_limite=data.get('fecha_limite') or None,
                id_pca=pca
            )
            
            return JsonResponse({
                'ok': True,
                'id': actividad.id_actividad,
                'nombre': actividad.nombre,
                'fecha_limite': str(actividad.fecha_limite) if actividad.fecha_limite else None
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        

@method_decorator(csrf_exempt, name='dispatch')
class EditarActividadView(View):
    def post(self, request, curso_id, asignatura_id, actividad_id):
        try:
            data = json.loads(request.body)
            actividad = Actividad.objects.get(pk=actividad_id)
            actividad.nombre = data.get('nombre', actividad.nombre)
            actividad.descripcion = data.get('descripcion', actividad.descripcion)
            actividad.fecha_limite = data.get('fecha_limite') or None
            actividad.save()
            return JsonResponse({
                'ok': True,
                'id': actividad.id_actividad,
                'nombre': actividad.nombre,
                'fecha_limite': str(actividad.fecha_limite) if actividad.fecha_limite else None
            })
        except Actividad.DoesNotExist:
            return JsonResponse({'error': 'Actividad no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        
@method_decorator(csrf_exempt, name='dispatch')
class EliminarActividadView(View):
    def post(self, request, curso_id, asignatura_id, actividad_id):
        try:
            actividad = Actividad.objects.get(pk=actividad_id)
            actividad.delete()
            return JsonResponse({'ok': True})
        except Actividad.DoesNotExist:
            return JsonResponse({'error': 'Actividad no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)