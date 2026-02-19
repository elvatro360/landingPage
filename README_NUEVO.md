# 🌐 Landing Page - Aplicación Django

> **Estado:** 🟡 Desarrollo | **Ambiente:** Proyecto de demostración  
> **Versión:** 1.0 | **Python:** 3.8+ | **Django:** 5.1.2

---

## 📋 Índice

- [¿Qué es?](#qué-es)
- [Quick Start](#-quick-start)
- [Documentación](#-documentación)
- [Estructura](#-estructura)
- [Características](#-características)
- [Seguridad](#-seguridad--crítico)
- [Despliegue](#-despliegue)
- [Contribuciones](#-contribuciones)

---

## 📌 ¿Qué es?

Landing page desarrollada con **Django 5.1.2** como micro-sitio de presentación con:
- ✅ Homepage atractiva
- ✅ Página de información (about)
- ✅ Formulario de contacto funcional
- ✅ Tema oscuro/claro (cliente)
- ✅ Admin integrado de Django
- ✅ Base de datos SQLite (desarrollo)

**Caso de uso:** Demostración, portfolio, proyectos pequeños.

---

## 🚀 Quick Start

### 1. Requisitos Previos
```bash
# Verificar Python
python --version    # Mínimo 3.8

# Verificar pip
pip --version
```

### 2. Clonar y Configurar
```bash
# Clonar repositorio
cd landingPage

# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requiriments.txt

# Aplicar migraciones
python manage.py migrate

# Crear superusuario (admin)
python manage.py createsuperuser
```

### 3. Ejecutar
```bash
python manage.py runserver

# Acceder a:
# http://localhost:8000/           (Homepage)
# http://localhost:8000/about/     (Información)
# http://localhost:8000/contacto/  (Formulario)
# http://localhost:8000/admin/     (Panel admin)
```

---

## 📚 Documentación

### Documentos Técnicos

| Documento | Contenido | Propósito |
|-----------|----------|----------|
| **[MEMORIA_TECNICA.md](MEMORIA_TECNICA.md)** | Arquitectura, componentes, flujos | Entender el sistema |
| **[SEGURIDAD.md](SEGURIDAD.md)** | Vulnerabilidades y recomendaciones | Preparar para producción |

### Guía de Lectura por Rol

**👨‍💻 Desarrollador:**
1. Quick Start (arriba)
2. Estructura del Proyecto
3. MEMORIA_TECNICA.md

**🔒 DevOps/Seguridad:**
1. SEGURIDAD.md (checklist de críticos)
2. Sección Despliegue

**📊 Product Manager:**
1. ¿Qué es? (arriba)
2. Características
3. Roadmap

---

## 📁 Estructura

```
landingPage/
├── 📄 manage.py                    ← CLI principal de Django
├── 📄 db.sqlite3                   ← BD (desarrollo)
├── 📄 requiriments.txt             ← Dependencias
│
├── 📁 mysite/                      ← Configuración proyecto
│   ├── settings.py                 ← ⚠️ Revisar seguridad
│   ├── urls.py                     ← Rutas principales
│   ├── wsgi.py                     ← Interfaz WSGI
│   └── asgi.py                     ← Interfaz ASGI
│
├── 📁 myapp/                       ← Aplicación principal
│   ├── views.py                    ← Vistas (4 rutas)
│   ├── forms.py                    ← Formulario contacto
│   ├── models.py                   ← Modelo ContactMessage
│   ├── urls.py                     ← Rutas app
│   ├── admin.py                    ← Configuración admin
│   │
│   ├── 📁 templates/
│   │   ├── base.html               ← Plantilla base
│   │   ├── hello_world.html        ← Homepage
│   │   ├── about.html              ← Info
│   │   ├── legal.html              ← Términos
│   │   ├── contacto.html           ← Formulario
│   │   └── contacto_success.html   ← Confirmación
│   │
│   ├── 📁 static/
│   │   ├── styles.css              ← Estilos base
│   │   ├── dark.css                ← Tema oscuro
│   │   ├── light.css               ← Tema claro
│   │   └── theme.js                ← Lógica de tema
│   │
│   └── 📁 migrations/              ← Migraciones BD
│       └── 0001_initial.py
│
├── 🔐 MEMORIA_TECNICA.md           ← Documentación técnica
├── 🔐 SEGURIDAD.md                 ← Análisis de seguridad
└── venv/                           ← Entorno virtual
```

---

## ✨ Características

### Frontend
- ✅ Diseño responsivo
- ✅ Tema oscuro/claro dinámico (localStorage)
- ✅ Formulario de contacto con validación
- ✅ CSS modular (base + temas)

### Backend
- ✅ Vistas Django (4 páginas + contacto)
- ✅ ORM con modelo ContactMessage
- ✅ Validación de formularios
- ✅ Admin de Django integrado
- ✅ Guardado de mensajes en BD

### Seguridad (Actual)
- ✅ CSRF protection (middleware)
- ✅ XSS auto-escape (plantillas)
- ✅ SQL injection prevention (ORM)
- ❌ Falta: HTTPS, rate limiting, CSP

---

## 🔐 SEGURIDAD ⚠️ CRÍTICO

### ⛔ NO APTO PARA PRODUCCIÓN

Encontradas **11 vulnerabilidades**:
- 🔴 **3 Críticas:** SECRET_KEY expuesta, DEBUG=True, Sin HTTPS
- 🔴 **4 Altas:** SQLite (producción), Sin rate limiting
- 🟡 **4 Medias:** Sin CSP, Sin logging, etc.

### ✅ Próximos Pasos (Antes de Producción)

**Inmediatos (Críticos):**
1. `settings.py`: Mover `SECRET_KEY` a variable de entorno
2. Cambiar `DEBUG = False`
3. Configurar HTTPS y certificado
4. Migrar a PostgreSQL

**Recomendados:**
5. Implementar rate limiting en contacto
6. Agregar Content Security Policy (CSP)
7. Sanitizar entrada (bleach)
8. Configurar monitoreo (Sentry)

**Ver detalles:** [`SEGURIDAD.md`](SEGURIDAD.md)

---

## 🚀 Despliegue

### Desarrollo Local ✅ (Ya funciona)

```bash
python manage.py runserver
# http://localhost:8000
```

### Staging/Testing 🟡 (Requiere cambios)

```bash
DEBUG = False
ALLOWED_HOSTS = ['192.168.x.x', 'staging.com']
# Base de datos: PostgreSQL recomendado
# HTTPS: Certificado autofirmado (para testing)
```

### Producción ⛔ (Requiere mucho más)

```
Arquitectura recomendada:

┌─────────┐
│ Cliente │ (HTTPS)
└────┬────┘
     │
┌────▼────────────────────┐
│ NGINX (Proxy, SSL/TLS)  │
└────┬────────────────────┘
     │
┌────▼──────────────────┐
│ Gunicorn (3-4 workers)│
└────┬──────────────────┘
     │
┌────▼──────────────┐
│ PostgreSQL (BD)   │
└───────────────────┘
```

**Proveedores recomendados:**
- 🟢 Heroku (simplest)
- 🟢 DigitalOcean (best value)
- 🟢 AWS (scale)
- 🟢 PythonAnywhere (Django-native)

### Checklist Pre-Despliegue

- [ ] `python manage.py check --deploy` (pasa)
- [ ] SECRET_KEY en `.env`
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS configurado
- [ ] HTTPS/certificado SSL
- [ ] BD migrada a PostgreSQL
- [ ] Backup automático
- [ ] Monitoreo habilitado (Sentry)

**Ver sección de seguridad en [SEGURIDAD.md](SEGURIDAD.md)**

---

## 👥 Contribuciones

### Reportar Issues
1. Abre un issue en GitHub
2. Describe el problema
3. Incluye pasos para reproducir

### Contribuir Código
1. Fork el repositorio
2. Crea rama: `git checkout -b feature/mi-feature`
3. Commit: `git commit -am "Descripción clara"`
4. Push: `git push origin feature/mi-feature`
5. Pull Request

### Sugerencias de Mejora

**Near-term (1-2 sprints):**
- [ ] CAPTCHA en formulario
- [ ] Envío de email en contacto
- [ ] Tests unitarios (views, forms)
- [ ] Validación mejorada

**Medium-term (1-2 meses):**
- [ ] Blog/noticias
- [ ] Carrito de productos
- [ ] Integración con Stripe/PayPal
- [ ] API REST

**Long-term (roadmap):**
- [ ] Migración a SPA (React/Vue)
- [ ] PWA capabilities
- [ ] Internacionalización (i18n)

---

## 📊 Estadísticas del Proyecto

| Métrica | Valor |
|---------|-------|
| **Líneas de código** | ~200 |
| **Plantillas** | 6 |
| **Vistas** | 4 funciones |
| **Modelos** | 1 (ContactMessage) |
| **Rutas** | 5 |
| **Dependencias** | 1 principal (Django) |
| **Tamaño BD** | <1 MB |
| **Tiempo de setup** | ~5 min |

---

## 🔧 Configuración Rápida

### Variables de Entorno (Crear `.env`)

```env
# ⚠️ NO COMMITEAR ESTE ARCHIVO

# Seguridad
SECRET_KEY=tu-clave-nueva-muy-larga-aqui
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,tudominio.com

# Base de datos (si usas PostgreSQL)
DATABASE_URL=postgresql://user:pass@localhost/dbname

# Email (para formulario)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password

# Seguridad adicional
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Cargar variables en `settings.py`

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')
```

**Instalar decouple:**
```bash
pip install python-decouple
# Agregar a requiriments.txt
```

---

## 📞 Soporte

| Recurso | Enlace |
|---------|--------|
| **Documentación Django** | https://docs.djangoproject.com/ |
| **OWASP Security** | https://owasp.org/www-project-top-ten/ |
| **Django Security** | https://docs.djangoproject.com/en/5.0/topics/security/ |

---

## 📝 Changelog

### v1.0 - 2024
- ✅ Setup inicial Django
- ✅ 4 vistas principales
- ✅ Formulario de contacto
- ✅ Tema oscuro/claro
- ⚠️ Falta seguridad para producción

### v1.1 (Próximo)
- [ ] Migrar a PostgreSQL
- [ ] Implementar HTTPS
- [ ] Rate limiting
- [ ] Tests unitarios

---

## ⚖️ Licencia

[Especificar tu licencia aquí - MIT, Apache 2.0, etc.]

---

## 👨‍💼 Autor

**Fernando Pérez**  
Portfolio: [tu-sitio.com]  
GitHub: [@tuusuario]  
Email: tu@email.com

---

## 🎯 Resumen

- ✅ **¿Funciona en desarrollo?** Sí, completamente
- ⚠️ **¿Está listo para producción?** NO - Requiere cambios de seguridad
- 📊 **¿Dificultad de arreglar?** Media (1-2 días)
- 🚀 **¿Vale la pena migrar?** Sí, es rápido

**Próximo paso recomendado:** Leer [SEGURIDAD.md](SEGURIDAD.md) y hacer los cambios críticos.

---

<div align="center">

**[📖 MEMORIA_TECNICA.md](MEMORIA_TECNICA.md)** · **[🔐 SEGURIDAD.md](SEGURIDAD.md)**

Última actualización: 2024  
Estado: 🟡 Activo en desarrollo

</div>
