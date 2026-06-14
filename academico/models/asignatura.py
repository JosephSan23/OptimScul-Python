from django.db import models

class Asignatura(models.Model):
    id_asignatura = models.AutoField(primary_key=True)
    colegio = models.ForeignKey('Colegio', models.DO_NOTHING)
    nombre_asignatura = models.CharField(max_length=50)
    
    class Meta:
        managed = False
        db_table = 'asignatura'
        
    def __str__(self):
        return self.nombre_asignatura