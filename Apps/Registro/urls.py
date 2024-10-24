from django.urls import path

from .import views
from .views import *

urlpatterns = [
    path("", views.registro,name='registro'),
    # Otras rutas que puedas tener
]