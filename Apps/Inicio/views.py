from django.shortcuts import render
from Apps.Blog.models import Publicacion  

def inicio(request):
    publicaciones_recientes = Publicacion.objects.order_by('-created_at')[:5]  # Últimas 5 publicaciones
    publicaciones_destacadas = Publicacion.objects.filter(destacada=True).order_by('-created_at')[:5]  # Primeras 5 destacadas
    return render(request, 'inicio.html', {'publicaciones_recientes': publicaciones_recientes, 'publicaciones_destacadas': publicaciones_destacadas})

def acerca_de(request):
    return render(request, 'acerca_de.html')