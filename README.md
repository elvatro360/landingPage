# 🏠 Landing Page: Crea una Página Profesional

> Aprende Django construyendo una página de bienvenida

---

## 📑 Índice Rápido

- [¿Qué es Django?](#qué-es-django)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instala y Configura](#instala-y-configura)
- [Crea Tu Primera Página](#crea-tu-primera-página)
- [Agrega Formularios](#agrega-formularios)
- [Desafíos](#desafíos)

---

## ❓ ¿Qué es Django?

### Django vs Flask

```
Flask:    Pequeño y flexible (como bicicleta)
          └─ Haces todo tú mismo

Django:   Grande y completo (como auto)
          └─ Muchas cosas ya vienen hechas
```

### ¿Por Qué Aprender Django?

```
✅ Completo: Todo incluido (BD, admin, seguridad)
✅ Estructurado: Carpetas y archivos organizados
✅ Robusto: Usado por empresas grandes
✅ Seguro: Protecciones contra ataques comunes
✅ Escalable: Crece con tu proyecto
```

---

## 📂 Estructura del Proyecto

### Carpetas Importantes

```
landing_page/
├── manage.py              ← Comando mágico
├── requirements.txt       ← Dependencias
├── mysite/                ← Configuración del proyecto
│   ├── settings.py       ← Configuración (BD, apps)
│   ├── urls.py           ← Rutas principales
│   └── wsgi.py           ← Para despliegue
├── myapp/                 ← Tu aplicación
│   ├── models.py         ← Base de datos
│   ├── views.py          ← Lógica
│   ├── urls.py           ← Rutas de app
│   └── templates/        ← HTML
├── static/                ← CSS, JS, imágenes
└── venv/                  ← Ambiente virtual
```

### Flujo de Datos

```
Usuario → URL → Django → views.py → templates/ → Página HTML

Ejemplo:
1. Escribes: http://localhost:8000/
2. Django mira urls.py: "¿Quién maneja /?"
3. Encuentra: views.py función home()
4. Función devuelve: templates/home.html
5. Se muestra en tu navegador
```

---

## 🚀 Instala y Configura

### Paso 1: Instalar Django
```bash
pip install django
```

### Paso 2: Crear Proyecto
```bash
django-admin startproject mysite
cd mysite
```

### Paso 3: Crear App
```bash
python manage.py startapp myapp
```

### Paso 4: Configurar App

En `mysite/settings.py`, agrega en INSTALLED_APPS:
```python
INSTALLED_APPS = [
    # ... otras apps
    'myapp',  # ← Agrega esto
]
```

### Paso 5: Crear Base de Datos
```bash
python manage.py migrate
```

### Paso 6: Ejecutar
```bash
python manage.py runserver

# Verás:
# Starting development server at http://127.0.0.1:8000/
```

---

## 🎨 Crea Tu Primera Página

### Paso 1: Crear Vista

En `myapp/views.py`:
```python
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>¡Bienvenido!</h1>")
```

### Paso 2: Crear Ruta

En `myapp/urls.py` (crear archivo):
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
```

### Paso 3: Conectar Rutas

En `mysite/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # ← Agrega esto
]
```

### Paso 4: Probar
```bash
python manage.py runserver
# Abre: http://localhost:8000
```

---

## 📝 Agrega Formularios

### Paso 1: Modelo de Contacto

En `myapp/models.py`:
```python
from django.db import models

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Mensaje de {self.nombre}"
```

### Paso 2: Migrar Base de Datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### Paso 3: Formulario HTML

En `myapp/templates/contacto.html`:
```html
<h1>Formulario de Contacto</h1>
<form method="POST" action="/contacto/">
    {% csrf_token %}
    
    <label>Nombre:</label>
    <input type="text" name="nombre" required>
    
    <label>Email:</label>
    <input type="email" name="email" required>
    
    <label>Mensaje:</label>
    <textarea name="mensaje" required></textarea>
    
    <button type="submit">Enviar</button>
</form>
```

### Paso 4: Vista para Procesar

En `myapp/views.py`:
```python
def contacto(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        mensaje = request.POST['mensaje']
        
        # Guardar en BD
        Contacto.objects.create(
            nombre=nombre,
            email=email,
            mensaje=mensaje
        )
        
        return HttpResponse("¡Mensaje enviado! Gracias.")
    
    return render(request, 'contacto.html')
```

### Paso 5: Agregar Ruta

En `myapp/urls.py`:
```python
urlpatterns = [
    path('', views.home, name='home'),
    path('contacto/', views.contacto, name='contacto'),  # ← Agrega
]
```

---

## 🎯 Desafíos

### Fácil ⭐
```
1. Crea 3 páginas (home, about, services)
2. Conecta con nav HTML
3. Agrega CSS básico
```

### Medio ⭐⭐
```
1. Crea modelo Blog
2. Formulario para crear posts
3. Muestra lista de posts
```

### Difícil ⭐⭐⭐
```
1. Crea sistema de comentarios
2. Usuarios pueden comentar posts
3. Mostrar comentarios en página
```

---

## 🔐 Panel Admin

Django tiene algo especial: ¡panel administrativo automático!

### Crear Usuario Admin
```bash
python manage.py createsuperuser
# Te pide: usuario, email, contraseña
```

### Registrar Modelo

En `myapp/admin.py`:
```python
from django.contrib import admin
from .models import Contacto

admin.site.register(Contacto)
```

### Acceder

1. Abre: http://localhost:8000/admin
2. Usa usuario/contraseña creados
3. ¡Gestiona tus datos sin código!

---

## 📚 Conceptos Importantes

### Model (M en MVT)
```python
Representa datos en la base de datos

class Producto(models.Model):
    nombre = CharField()      # Texto corto
    descripcion = TextField() # Texto largo
    precio = DecimalField()   # Número con decimales
    fecha = DateField()       # Fecha
```

### View (V en MVT)
```python
Lógica que decide qué mostrar

def home(request):
    # Procesa request
    # Retorna respuesta
    return render(request, 'template.html', contexto)
```

### Template (T en MVT)
```html
HTML con variables de Python

<h1>{{ titulo }}</h1>
{% for item in lista %}
    <p>{{ item }}</p>
{% endfor %}
```

### URL
```python
Conecta ruta con vista

path('ruta/', views.funcion, name='nombre'),
```

---

## 🏁 Siguientes Pasos

### Mejoras
```
1. Template base reutilizable
   → {% extends 'base.html' %}
   
2. CSS profesional
   → Bootstrap, Tailwind
   
3. Autenticación de usuarios
   → Django tiene built-in
   
4. Base de datos real
   → PostgreSQL, MySQL
```

### Próximo Proyecto
```
CRUD (proyecto siguiente)
└─ Versión más completa de este
```

---

## 📖 Aprende Más

### Documentación
- 📖 [Django Oficial](https://www.djangoproject.com/)
- 📖 [Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)

### Cursos
- 🎥 "Django for Beginners"
- 🎥 "Complete Django Course"

---

## 🎓 Checklist

- [ ] Instalé Django
- [ ] Creé proyecto y app
- [ ] Hice primera página
- [ ] Creé modelo y migración
- [ ] Hice formulario de contacto
- [ ] Guardé datos en BD
- [ ] Accedí a panel admin

**Si marcaste todo ✓ → ¡Ya sabes Django! 🎉**

---

<div align="center">

## ✅ ¡Excelente!

### Aprendiste Django

**Siguiente proyecto:**

[📊 CRUD](../proyectocrud/README.md) - Operaciones Completas de BD

---

*Amigable | Paso a paso | Profesional*

</div>
