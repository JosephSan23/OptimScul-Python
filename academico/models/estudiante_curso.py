from django.db import models
from .estudiante import Estudiante
from .curso import Curso

class EstudianteCurso(models.Model):
    # Opciones para el campo ENUM de la base de datos externa
    ESTADO_CHOICES = [
        ('inscrito', 'Inscrito'),
        ('retirado', 'Retirado'),
        ('graduado', 'Graduado'),
    ]

    # Relaciones ForeignKey apuntando a tus modelos existentes
    # Añadimos primary_key=True para evitar el error de columna 'id' fantasma
    id_estudiante = models.ForeignKey(
        Estudiante, 
        on_delete=models.CASCADE, 
        db_column='id_estudiante',
        primary_key=True
    )
    id_curso = models.ForeignKey(
        Curso, 
        on_delete=models.CASCADE, 
        db_column='id_curso'
    )
    
    # Campo ENUM mapeado como CharField con opciones
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='inscrito'
    )
    
    # Campos de fecha y hora
    fecha_inscripcion = models.DateTimeField(null=True, blank=True)
    fecha_retiro = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'estudiante_curso'  # Nombre exacto de la tabla en MySQL
        # Evita que Django intente crear o modificar la estructura de esta tabla
        managed = False  
        # Simulación de la restricción única compuesta
        unique_together = (('id_estudiante', 'id_curso'),)

    def __str__(self):
        return f"{self.id_estudiante} - {self.id_curso} ({self.estado})"