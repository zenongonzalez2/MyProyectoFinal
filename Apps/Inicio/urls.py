from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 


urlpatterns = [
    path('', views.inicio, name='home'),
    path('inicio/', views.inicio, name='inicio'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('acerca_de/', views.acerca_de, name='acerca_de'),

]
