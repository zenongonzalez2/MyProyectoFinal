from django.urls import path
from . import views
from.views import *

urlpatterns = [
    path('', views.blog, name='blog'),
    path('categoria/<int:cat_id>/', views.categoria, name='categoria'),
    path('publicacion/<int:publicacion_id>/', views.detalle_publicacion, name='detalle_publicacion'),
    path('publicacion/cargar/', views.cargar_publicacion, name='cargar_publicacion'),
    path('publicacion/<int:publicacion_id>/editar/', views.editar_publicacion, name='editar_publicacion'),
    path('publicacion/<int:publicacion_id>/eliminar/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('comentario/<int:comentario_id>/eliminar/', views.eliminar_comentario, name='eliminar_comentario'),
    
]
