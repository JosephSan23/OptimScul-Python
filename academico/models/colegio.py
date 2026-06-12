from django.db import models

class Colegio(models.Model):
    id_colegio = models.AutoField(primary_key=True)
    nombre_colegio = models.CharField(max_length=100)
    nit = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    correo_institucional = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=7)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)
    nota_minima = models.DecimalField(max_digits=4, decimal_places=2)
    nota_maxima = models.DecimalField(max_digits=4, decimal_places=2)
    nota_aprobacion = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        # Managed: False le dice a django que ya tengo creada una bd entonces que no la modifique.
        managed: False
        db_table = 'colegio'
        
    def __str__(self):
        return self.nombre_colegio