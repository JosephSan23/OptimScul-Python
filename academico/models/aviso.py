from django.db import models

class Aviso(models.Model):
    id_aviso = models.AutoField(primary_key=True)
    
    autor = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, null=True, blank=True)
    asignatura = models.ForeignKey('Asignatura', on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        db_table = 'aviso'
        ordering = ['-fecha_publicacion']
        managed = False 