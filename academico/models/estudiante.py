from django.db import models
from .usuario import Usuario  # importa tu modelo directamente

class Estudiante(models.Model):
    id_estudiante = models.OneToOneField(
        Usuario,  # ← tu modelo, no AUTH_USER_MODEL
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_estudiante'
    )
    fecha_ingreso = models.DateField(db_column='fecha_ingreso')

    class Meta:
        db_table = 'estudiante'
        managed = False

    def __str__(self):
        return f"Estudiante: {self.id_estudiante.primer_nombre}"