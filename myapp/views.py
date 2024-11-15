from django.shortcuts import render
from django.http import HttpResponse
from myapp.forms import ContactForm
from .models import ContactMessage

def hello_world(request):
    return render(request, 'hello_world.html')

def about(request):
    return render(request, 'about.html')

def legal(request):
    return render(request, 'legal.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        print(request.POST) # Debugging
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            correo = form.cleaned_data['correo']
            mensaje = form.cleaned_data['mensaje']
            # Crear un objeto de mensaje de contacto y guardarlo en la base de datos
            ContactMessage.objects.create(
                nombre=nombre,
                correo=correo,
                mensaje=mensaje
            )
            return render(request, 'contacto_success.html')
        else:
            print(form.errors) # Debugging
    else:
        form = ContactForm()
    return render(request, 'contacto.html', {'form': form})