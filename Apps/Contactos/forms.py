from django import forms


class ContactForm(forms.Form):
    nombre =forms.CharField(label="Nombre",required=True)
    apellido = forms.CharField(label="Apellido",required=True)
    email = forms.CharField(label="Correo Electronico:",required=True)