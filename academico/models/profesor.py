from django.db import models

class Profesor(models.Model):
    id_profesor = models.OneToOneField('Usuario', models.DO_NOTHING, db_column='id_profesor', primary_key=True)
    titulo_academico = models.CharField(max_length=100, blank=True, null=True)
    experiencia_anios = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profesor'

    def __str__(self):
        return f"Profesor: {self.id_profesor.primer_nombre} {self.id_profesor.primer_apellido}"