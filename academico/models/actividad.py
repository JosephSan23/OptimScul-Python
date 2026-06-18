from django.db import models

class Actividad(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    fecha_limite = models.DateField(null=True, blank=True)
    
    # Llave foránea a la tabla intermedia que une Profesor, Curso y Asignatura
    id_pca = models.ForeignKey('ProfesorCursoAsignatura', on_delete=models.CASCADE, db_column='id_pca')
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'actividad'
        ordering = ['-created_at']
        managed = False