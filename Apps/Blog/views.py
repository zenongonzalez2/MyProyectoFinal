from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect, render
from .models import Publicacion, Categoria, Comentario, PerfilColaborador
from .forms import ComentarioForm, PublicacionForm  # Asegúrate de importar el formulario de publicación
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models.signals import post_save 
from django.contrib.auth.models import User

# Crear tus vistas aquí.
def blog(request):
    publicaciones = Publicacion.objects.order_by('-created_at')  # Ordenar por las más recientes
    categorias = Categoria.objects.all()
    return render(request, "blog.html", {"publicaciones": publicaciones, "categorias": categorias})

def categoria(request, cat_id):
    categorias = Categoria.objects.all()
    categoria = Categoria.objects.get(id=cat_id)
    publicaciones = Publicacion.objects.filter(categorias=categoria).order_by('-created_at')  # Ordenar por las más recientes
    return render(request, "categoria.html", {'categorias': categorias, 'cat_id': cat_id, 'publicaciones': publicaciones})

def home(request):
    publicaciones_recientes = Publicacion.objects.order_by('-created_at')[:5]  # Últimas 5 publicaciones
    publicaciones_destacadas = Publicacion.objects.filter(destacada=True).order_by('-created_at')[:5]  # Primeras 5 destacadas
    return render(request, 'inicio.html', {'publicaciones_recientes': publicaciones_recientes, 'publicaciones_destacadas': publicaciones_destacadas})

def detalle_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    comentarios = publicacion.comentarios.all()

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.publicacion = publicacion
            comentario.autor = request.user
            comentario.save()
            return redirect('detalle_publicacion', publicacion_id=publicacion.id)
    else:
        form = ComentarioForm()

    return render(request, 'detalle_publicacion.html', {'publicacion': publicacion, 'comentarios': comentarios, 'form': form})


@login_required
@permission_required('app.puede_agregar_colaborador', raise_exception=True)  # Asegúrate de tener este permiso configurado
def asignar_colaborador(request):
    usuarios = User.objects.exclude(perfilcolaborador__isnull=False)  # Excluir usuarios que ya son colaboradores
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        PerfilColaborador.objects.create(user=user)
        # Agregar permisos específicos al nuevo colaborador si es necesario
        return redirect('lista_colaboradores')  # Redirige a una lista de colaboradores o a la página deseada
    
    return render(request, 'asignar_colaborador.html', {'usuarios': usuarios})


@login_required
@permission_required('blog.puede_editar_publicacion', raise_exception=True)
def editar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect('detalle_publicacion', publicacion_id=publicacion.id)  # Redirigir a la publicación editada
    else:
        form = PublicacionForm(instance=publicacion)

    return render(request, 'editar_publicacion.html', {'form': form, 'publicacion': publicacion})

@login_required
@permission_required('blog.puede_agregar_publicacion', raise_exception=True)
def cargar_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.autor = request.user  # Asigna el autor como el usuario que está logueado
            publicacion.save()
            return redirect('blog')  # Redirige al blog o a otra página que prefieras
    else:
        form = PublicacionForm()

    return render(request, 'cargar_publicacion.html', {'form': form})

@login_required
@permission_required('blog.puede_eliminar_publicacion', raise_exception=True)
def eliminar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    
    if request.method == 'POST':
        publicacion.delete()
        return redirect('blog')  # Redirige al blog o donde consideres necesario

    return render(request, 'eliminar_publicacion.html', {'publicacion': publicacion})


@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if comentario.autor != request.user and not request.user.has_perm('blog.puede_eliminar_comentario'):
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para eliminar este comentario.'})

    if request.method == 'POST':
        comentario.delete()
        return redirect('detalle_publicacion', publicacion_id=comentario.publicacion.id)
    return render(request, 'eliminar_comentario.html', {'comentario': comentario})


@receiver(post_save, sender=User)
def crear_perfil_colaborador(sender, instance, created, **kwargs):
    if created:
        PerfilColaborador.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil_colaborador(sender, instance, **kwargs):
    instance.perfilcolaborador.save()