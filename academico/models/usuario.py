from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    colegio = models.ForeignKey('Colegio', models.DO_NOTHING)
    rol = models.CharField(max_length=13)
    primer_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50, blank=True, null=True)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    tipo_documento = models.CharField(max_length=2, blank=True, null=True)
    documento = models.CharField(unique=True, max_length=20)
    username = models.CharField(max_length=30)
    correo = models.CharField(unique=True, max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    contrasena = models.CharField(max_length=255)
    estado = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'usuario'

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido} ({self.rol})"