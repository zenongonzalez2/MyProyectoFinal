from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # Importar correctamente

class Categoria(models.Model):
    titulo = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.titulo

class Publicacion(models.Model):
    titulo = models.CharField(max_length=300)
    contenido = models.TextField(max_length=5000)
    imagen = models.ImageField(upload_to="publicaciones")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    categorias = models.ManyToManyField(Categoria)
    destacada = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Publicacion"
        verbose_name_plural = "Publicaciones"
        permissions = [
            ("puede_agregar_publicacion", "Puede agregar publicaciones"),
            ("puede_editar_publicacion", "Puede editar publicaciones"),
            ("puede_eliminar_publicacion", "Puede eliminar publicaciones"),
        ]

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.CharField(max_length=5000)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("puede_eliminar_comentario", "Puede eliminar comentarios"),
        ]

    def __str__(self):
        return f'Comentado por {self.autor} on {self.publicacion}'

class PerfilColaborador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    es_colaborador = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
