# Create your models here.

from django.db import models

class Post(models.Model):
    titulo = models.CharField(max_length=200)  # Campo para el título del post
    contenido = models.TextField()  # Campo para el contenido del post
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación (automática)

    def __str__(self):
        return self.titulo  # Devuelve el título del post cuando se representa el objeto