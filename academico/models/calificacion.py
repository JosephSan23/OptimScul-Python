from django.db import models

class Calificacion(models.Model):
    id_calificacion = models.AutoField(primary_key=True)
    colegio_id = models.IntegerField()
    
    id_estudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE, db_column='id_estudiante')
    
    id_actividad = models.ForeignKey('Actividad', on_delete=models.CASCADE, db_column='id_actividad')
    
    estado = models.CharField(max_length=20)  # Para manejar el ENUM ('entregado', 'sin_entregar', etc.)
    archivo_url = models.CharField(max_length=500, null=True, blank=True)
    nota = models.DecimalField(max_length=4, decimal_places=2, max_digits=4, null=True, blank=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'calificacion'
        managed = False