# 📘 Memoria Técnica - Landing Page Django

## 🎯 Resumen Ejecutivo

**Proyecto:** Landing Page - Aplicación Django  
**Tipo:** Micro-sitio de presentación con formulario de contacto  
**Stack:** Django 5.1.2 + SQLite + CSS/JS estático  
**Estado:** Desarrollo (⚠️ No apto para producción sin cambios)  
**Última actualización:** 2024

---

## 📋 Índice

1. [Arquitectura General](#arquitectura-general)
2. [Componentes Principales](#componentes-principales)
3. [Flujo de Datos](#flujo-de-datos)
4. [Dependencias](#dependencias)
5. [Base de Datos](#base-de-datos)
6. [Configuración](#configuración)
7. [Despliegue](#despliegue)

---

## 🏗️ Arquitectura General

### Patrón de Diseño
- **Patrón:** MVT (Model-View-Template)
- **Framework:** Django 5.0+
- **Tipo:** Aplicación web tradicional (server-side rendering)

### Capas

```
┌─────────────────────────────────────────┐
│         Frontend (HTML/CSS/JS)          │
│  (Plantillas Django + Assets estáticos) │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│      Capa de Aplicación (Django)        │
│  URLs → Views → Forms → Templates       │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│      Capa de Datos (SQLite)             │
│  Modelos ORM → Base de datos            │
└─────────────────────────────────────────┘
```

---

## 🧩 Componentes Principales

### 1. Configuración Central (`mysite/settings.py`)

```python
BASE_DIR = Project root
SECRET_KEY = Clave secreta para sesiones y CSRF
DEBUG = True/False (¡Importante para producción!)
ALLOWED_HOSTS = Hosts permitidos
INSTALLED_APPS = Apps registradas
MIDDLEWARE = Pipeline de procesamiento
DATABASES = Configuración de BD
STATIC_URL = URL para servir estáticos
```

**Estado actual:**
- ✅ Middleware de seguridad configurado
- ⚠️ `DEBUG=True` (NO para producción)
- ⚠️ `SECRET_KEY` expuesta en el código
- ✅ `ALLOWED_HOSTS` configurado para desarrollo

### 2. Aplicación Principal (`myapp/`)

#### Vistas (`views.py`)
```python
- hello_world()      → Página de inicio
- about()            → Página de información
- legal()            → Página legal
- contact_view()     → Formulario de contacto (POST/GET)
```

#### Formularios (`forms.py`)
```python
- ContactForm
  ├── nombre (CharField, max_length=100)
  ├── correo (EmailField)
  └── mensaje (CharField, widget=Textarea)
```

**Validación:** ✅ Campo email valida formato  
**Sanitización:** ⚠️ No sanitiza HTML/scripts en mensaje

#### Modelos (`models.py`)
```python
- ContactMessage
  ├── nombre
  ├── correo
  ├── mensaje
  └── created_at (timestamp)
```

#### Plantillas (`templates/myapp/`)
```
├── base.html              (Estructura común)
├── hello_world.html       (Homepage)
├── about.html             (Información)
├── legal.html             (Términos legales)
├── contacto.html          (Formulario)
└── contacto_success.html  (Confirmación)
```

---

## 🔄 Flujo de Datos

### Flujo del Formulario de Contacto

```
1. GET /contacto/
   └─→ contact_view() renderiza formulario vacío
       └─→ contacto.html

2. Usuario llena formulario y envía POST
   └─→ contact_view(request.POST)
       ├─→ Valida ContactForm
       ├─→ Si válido: ContactMessage.objects.create()
       │   └─→ Guarda en BD
       ├─→ Renderiza contacto_success.html
       └─→ Si error: Re-renderiza con errores

3. Datos guardados en ContactMessage
   └─→ Accesible desde admin (/admin/)
```

### Flujo de Cambio de Tema (Cliente)

```
1. Página carga base.html
2. JS (theme.js) se ejecuta
3. Verifica preferencia (localStorage o SO)
4. Inyecta CSS correspondiente
   ├─→ dark.css (modo oscuro)
   └─→ light.css (modo claro)
5. Guarda preferencia en localStorage
```

---

## 📦 Dependencias

### Stack Técnico

| Componente | Versión | Propósito |
|-----------|---------|----------|
| **Django** | 5.1.2 | Framework web |
| **Python** | 3.8+ | Lenguaje base |
| **SQLite** | 3.x | BD desarrollo |
| **asgiref** | 3.8.1 | Interfaz ASGI |
| **sqlparse** | 0.5.1 | Parser SQL |
| **tzdata** | 2024.2 | Datos de zona horaria |

### Dependencias de Desarrollo
```
virtualenv==20.25.1
distlib==0.3.8
platformdirs==4.2.0
filelock==3.13.1
```

### Estado de Seguridad de Dependencias
```
✅ Django 5.1.2 - Versión estable actual
⚠️ pytube==15.0.0 - NO USADO (eliminar si no se usa)
```

---

## 💾 Base de Datos

### Tabla: `myapp_contactmessage`

```sql
CREATE TABLE myapp_contactmessage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(254) NOT NULL,  -- Estándar para emails
    mensaje TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Características Actuales

- **Motor:** SQLite (archivo: `db.sqlite3`)
- **Ubicación:** `../db.sqlite3` (fuera del proyecto)
- **Tamaño:** Ideal para desarrollo (<100MB)
- **Concurrencia:** Limitada (no multiusuario)

### ⚠️ Limitaciones para Producción

```
SQLite NO ES RECOMENDABLE porque:
❌ Bloquea archivos (problemas de concurrencia)
❌ No tiene replicación
❌ Sin backup automático
❌ Sin autenticación de usuarios
❌ Limitado a ~140MB en tamaño
```

---

## ⚙️ Configuración

### Carpeta de Proyecto

```
landingPage/
├── manage.py                 ← Herramienta CLI Django
├── db.sqlite3               ← Base de datos
├── requiriments.txt         ← Dependencias
│
├── mysite/                  ← Configuración principal
│   ├── settings.py         ← Configuración Django
│   ├── urls.py             ← Rutas principales
│   ├── wsgi.py             ← Interfaz WSGI (producción)
│   └── asgi.py             ← Interfaz ASGI (async)
│
├── myapp/                   ← Aplicación de negocio
│   ├── views.py            ← Vistas
│   ├── forms.py            ← Formularios
│   ├── models.py           ← Modelos ORM
│   ├── urls.py             ← Rutas de app
│   ├── templates/          ← Plantillas HTML
│   └── static/             ← CSS, JS, imágenes
│
└── venv/                    ← Entorno virtual
```

### Archivos de Configuración Importantes

**`settings.py` - Configuración por entorno**

```python
# ⚠️ DESARROLLO (actual)
DEBUG = True
SECRET_KEY = 'django-insecure-...'  # EXPUESTA
ALLOWED_HOSTS = ['192.168.1.73', 'localhost']
DATABASES = {'sqlite3': 'db.sqlite3'}

# ✅ PRODUCCIÓN (debe ser)
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')  # Variable de entorno
ALLOWED_HOSTS = ['tudominio.com', 'www.tudominio.com']
DATABASES = {'postgresql': '...'}
```

**`urls.py` - Enrutamiento**

```python
path('admin/', admin.site.urls)
path('', views.hello_world)
path('about/', views.about)
path('legal/', views.legal)
path('contacto/', views.contact_view)
```

---

## 🚀 Despliegue

### Desarrollo Local

```bash
# 1. Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate          # Windows
source venv/bin/activate         # Linux/Mac

# 2. Instalar dependencias
pip install -r requiriments.txt

# 3. Migraciones
python manage.py migrate

# 4. Ejecutar servidor
python manage.py runserver
# Acceso: http://localhost:8000
```

### Requisitos para Producción

```
1. Servidor WSGI
   └─→ Gunicorn, uWSGI

2. Proxy inverso
   └─→ NGINX, Apache

3. Base de datos
   └─→ PostgreSQL, MySQL

4. Certificado SSL/TLS
   └─→ Let's Encrypt

5. Hosting
   └─→ AWS, Heroku, DigitalOcean, VPS
```

### Arquitectura de Producción Recomendada

```
┌─────────────────────────┐
│   Cliente (Navegador)   │
└────────────┬────────────┘
             │ HTTPS
     ┌───────▼────────┐
     │  NGINX         │  (Proxy, SSL termination)
     │  :80, :443     │
     └────────┬───────┘
              │
     ┌────────▼────────────┐
     │  Gunicorn           │  (3-4 workers)
     │  :8000 (privado)    │
     └────────┬────────────┘
              │
     ┌────────▼────────────┐
     │  PostgreSQL         │  (Base de datos)
     │  :5432 (privado)    │
     └─────────────────────┘
```

---

## 📊 Diagrama de Flujo General

```
HTTP Request
    │
    ▼
NGINX (proxy, SSL)
    │
    ▼
Gunicorn (WSGI app)
    │
    ▼
Django URL Router (urls.py)
    │
    ├─→ hello_world() ──→ Template ──→ HTML Response
    ├─→ about() ────────→ Template ──→ HTML Response
    ├─→ legal() ────────→ Template ──→ HTML Response
    │
    └─→ contact_view()
        ├─ GET ──→ ContactForm (vacío) ──→ contacto.html
        └─ POST ─→ Validar ─→ BD ──→ contacto_success.html
              │
              ▼
        ContactMessage (SQLite)
              │
              ▼
        Admin (Django)
```

---

## 🔐 Consideraciones de Seguridad

### Vulnerabilidades Identificadas ⚠️

1. **SECRET_KEY Expuesta** - En el código fuente
2. **DEBUG=True** - Expone información sensible
3. **Sin sanitización de entrada** - Riesgo XSS en mensaje
4. **Sin rate limiting** - Spam sin control
5. **Sin HTTPS configurado** - Tráfico sin cifrar
6. **Base de datos en desarrollo** - No segura para producción

### Próximos Pasos de Seguridad ✅

1. Variables de entorno para configuración sensible
2. Content Security Policy (CSP)
3. Rate limiting en formularios
4. CAPTCHA o verificación
5. Certificado SSL
6. Migración a PostgreSQL

---

## 📈 Métricas del Proyecto

| Métrica | Valor |
|---------|-------|
| **Líneas de código** | ~200 (views + forms) |
| **Plantillas** | 6 archivos |
| **Modelos** | 1 (ContactMessage) |
| **Vistas** | 4 funciones |
| **URLs** | 5 rutas |
| **Dependencias principales** | 1 (Django) |
| **Tamaño BD** | <1 MB |

---

## 🔄 Ciclo de Vida de Solicitud

```
1. Usuario accede http://localhost:8000/contacto/
2. Django router matchea: urlpatterns → contact_view
3. contact_view() verifica method (GET)
4. Crea ContactForm vacío
5. Renderiza 'contacto.html' con contexto {'form': form}
6. Template itera form.fields, renderiza inputs
7. HTML se envía a navegador
8. Usuario llena y envía (POST)
9. contact_view() recibe request.POST
10. Valida ContactForm(request.POST)
11. Si válido: Crea ContactMessage en BD
12. Renderiza 'contacto_success.html'
```

---

## 📞 Puntos de Contacto y Responsabilidades

| Componente | Responsabilidad | Riesgo |
|-----------|-----------------|--------|
| `views.py` | Lógica de negocio | Input validation |
| `forms.py` | Validación frontend | Bypass |
| `models.py` | Persistencia | SQL injection |
| `templates/` | Presentación | XSS |
| `settings.py` | Configuración | Exposición de secretos |

---

## 🎓 Conclusión

La aplicación es un **proyecto de demostración funcional** con una arquitectura clara basada en Django MVT. Para llevarla a producción, se requieren cambios significativos en seguridad, infraestructura y configuración.

**Ver:** [`SEGURIDAD.md`](SEGURIDAD.md) para recomendaciones específicas.
