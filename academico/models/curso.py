from django.db import models

class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    colegio = models.ForeignKey('Colegio', models.DO_NOTHING)
    nombre_curso = models.CharField(max_length=50)
    grado = models.IntegerField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    capacidad_maxima = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=8, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    tipo = models.CharField(max_length=9)

    class Meta:
        managed = False
        db_table = 'curso'

    def __str__(self):
        return self.nombre_curso