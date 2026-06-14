from django.db import models

class ProfesorCursoAsignatura(models.Model):
    id_pca = models.AutoField(primary_key=True)
    id_profesor = models.ForeignKey('Profesor', models.DO_NOTHING, db_column='id_profesor')
    id_curso = models.ForeignKey('Curso', models.DO_NOTHING, db_column='id_curso')
    id_asignatura = models.ForeignKey('Asignatura', models.DO_NOTHING, db_column='id_asignatura')

    class Meta:
        managed = False
        db_table = 'profesor_curso_asignatura'
        unique_together = (('id_profesor', 'id_curso', 'id_asignatura'),)

    def __str__(self):
        return f"{self.id_profesor} -> {self.id_curso} ({self.id_asignatura})"