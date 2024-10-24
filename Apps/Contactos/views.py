from django.shortcuts import redirect, render
from django.core.mail import EmailMessage
from .forms import ContactForm
from django.conf import settings

# Create your views here.

def contactos(request):
    form = ContactForm()
    
    if request.method == "POST":
        form = ContactForm(data=request.POST)
        
        if form.is_valid(): #Devuelve True si todos los datos son válidos y cumplen con las reglas definidas en el formulario; de lo contrario, devuelve False.
            nombre = request.POST.get("nombre")
            apellido = request.POST.get("apellido")
            email = request.POST.get("email")
     
            # Construir el mensaje
            subject = "This is a subject"
            body = f"Hola {nombre} {apellido},\n\nEspero que te encuentres bien. Gracias por ponerte en contacto con nostros. Si tienes alguna pregunta, no dudes en responder a este correo.\n\nSaludos cordiales,\n[Equipo Ciber Seguridad]"
            from_email = ""
            recipient_list = [email]
            
            mensaje = EmailMessage(
                subject,
                body,
                from_email,
                recipient_list,
            )
            
            try: 
                mensaje.send()
                return redirect("/contacto/?ok")
            except Exception as e:
                 print(f"Error al enviar el correo: {e}")
                 return redirect("/contacto/?not_ok")
                
    return render(request,"contactos.html",{"form":form})