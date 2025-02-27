from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'titulo', 'contenido', 'fecha_creacion']  # Los campos que deseas exponer en la API