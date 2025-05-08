from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    nombre = models.CharField(max_length=200)
    correo = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre} ({self.correo})"

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
