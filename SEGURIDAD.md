# 🔐 Guía de Seguridad - Landing Page Django

## ⚠️ Estado Actual: NO APTO PARA PRODUCCIÓN

Este documento detalla vulnerabilidades encontradas y recomendaciones de seguridad para el proyecto.

---

## 📋 Índice de Vulnerabilidades

1. [Críticas](#-críticas)
2. [Altas](#-altas)
3. [Medias](#-medias)
4. [Bajas](#-bajas)
5. [Checklist de Implementación](#checklist-de-implementación)

---

## 🔴 CRÍTICAS

### 1. SECRET_KEY Expuesta en Código Fuente

**Ubicación:** `mysite/settings.py` línea 23

```python
# ❌ INSEGURO
SECRET_KEY = 'django-insecure-r*f=_&l1h*b6$=lbz&z9oh%-i_wef2@-ia0a52vd^41^h-h#un'
```

**Riesgo:** 
- Django usa esta clave para firmar sesiones, CSRF, cookies
- Si se expone, atacante puede:
  - Falsificar sesiones
  - Bypass CSRF protection
  - Decriptar cookies
  - Ejecutar operaciones como usuario autenticado

**Impacto:** 🔥 **CRÍTICO** - Acceso total al sistema

**Solución:**

```python
# ✅ SEGURO - Usar variable de entorno
import os
from pathlib import Path

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'dev-key-only-for-development'  # Solo para desarrollo
)

# En producción, establecer:
# export SECRET_KEY="nueva-clave-segura-64-caracteres"
```

**Generar nueva clave segura:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())  # Genera: 'django-insecure-...'
```

**Paso a paso:**
1. Generar clave nueva: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
2. Guardar en archivo `.env` (no commitear)
3. Cargar en `settings.py` desde `os.environ`
4. En servidor: establecer variable de entorno

**Archivo: `.env` (GITIGNORE THIS)**
```
SECRET_KEY=django-insecure-nueva-clave-muy-larga-aqui
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

**Cargar en settings.py:**
```python
from decouple import config  # pip install python-decouple

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')
```

---

### 2. DEBUG=True en Producción

**Ubicación:** `mysite/settings.py` línea 26

```python
# ❌ INSEGURO
DEBUG = True
```

**Riesgo:**
- Expone stack traces completos con rutas internas
- Muestra variables de entorno parcialmente
- Revela estructura del proyecto
- Facilita reconocimiento de patrones de ataque

**Impacto:** 🔥 **CRÍTICO** - Information Disclosure

**Solución:**

```python
# ✅ SEGURO
DEBUG = False  # En producción

# O mejor: desde .env
DEBUG = config('DEBUG', default=False, cast=bool)
```

**Verificar antes de desplegar:**
```bash
python manage.py check --deploy
```

---

### 3. Sin Validación/Sanitización de Entrada

**Ubicación:** `myapp/forms.py` y `myapp/views.py`

```python
# ❌ RIESGO: Sin sanitizar mensaje
mensaje = form.cleaned_data['mensaje']
ContactMessage.objects.create(
    nombre=nombre,
    correo=correo,
    mensaje=mensaje  # ← Aquí podría haber HTML/JS
)
```

**Riesgo:**
- **XSS (Cross-Site Scripting):** `<script>alert('XSS')</script>`
- **SQL Injection:** Ya protegido por ORM Django (GOOD!)
- **HTML Injection:** En admin o si se renderiza sin escape

**Impacto:** 🔴 **ALTO** - Ejecución de código en navegador

**Solución Completa:**

```python
from django import forms
from django.utils.html import escape
import bleach

class ContactForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        strip=True,  # Elimina espacios antes/después
        widget=forms.TextInput(attrs={'required': 'required'})
    )
    correo = forms.EmailField(
        strip=True,
        widget=forms.EmailInput(attrs={'required': 'required'})
    )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={'required': 'required', 'rows': 5}),
        strip=True,
        max_length=2000  # Limita tamaño
    )
    
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        # Validar caracteres permitidos
        if not all(c.isalnum() or c.isspace() for c in nombre):
            raise forms.ValidationError("Nombre contiene caracteres inválidos")
        return nombre
    
    def clean_mensaje(self):
        mensaje = self.cleaned_data['mensaje']
        # Sanitizar con bleach si es necesario
        # SOLO si necesitas permitir HTML mínimo
        # mensaje = bleach.clean(mensaje, tags=[], strip=True)
        return mensaje
```

**En template (auto-escape habilitado):**
```django
<!-- ✅ Seguro: Django escapa automáticamente -->
<p>{{ contacto.mensaje }}</p>

<!-- ❌ INSEGURO: No hagas esto -->
<p>{{ contacto.mensaje|safe }}</p>
```

**Instalar bleach para sanitización:**
```bash
pip install bleach
# En requirements.txt
bleach==6.1.0
```

---

## 🔴 ALTAS

### 4. Sin HTTPS / TLS

**Ubicación:** Toda la aplicación

**Riesgo:**
- Tráfico sin cifrar (man-in-the-middle)
- Cookies/sesiones interceptables
- Credenciales en texto plano
- No cumple GDPR/normativas

**Impacto:** 🔴 **ALTO** - Interceptación de datos

**Solución:**

```python
# En settings.py (PRODUCCIÓN)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

**Configuración NGINX:**
```nginx
server {
    listen 443 ssl http2;
    server_name tudominio.com www.tudominio.com;
    
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    
    # Redirect HTTP → HTTPS
}

server {
    listen 80;
    server_name tudominio.com www.tudominio.com;
    return 301 https://$server_name$request_uri;
}
```

**Certificado Let's Encrypt:**
```bash
sudo certbot certonly --standalone -d tudominio.com -d www.tudominio.com
```

---

### 5. Base de Datos SQLite (No para Producción)

**Ubicación:** `mysite/settings.py` línea 77-82

```python
# ❌ PRODUCCIÓN INSEGURA
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}
```

**Problemas:**
- Sin autenticación de usuario
- Sin replicación/backup
- Bloquea archivos (bajo concurrencia)
- Inseguro para multiusuario
- Sin backup automático

**Impacto:** 🔴 **ALTO** - Pérdida de datos

**Solución - PostgreSQL:**

```python
# ✅ SEGURO - PostgreSQL en producción
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='landingpage'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

**Instalación PostgreSQL (Ubuntu/Debian):**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres createdb landingpage
sudo -u postgres createuser -P landingpage_user
# Grant privileges...
```

**Docker alternative:**
```yaml
version: '3'
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: landingpage
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
```

---

### 6. Sin Rate Limiting en Formulario

**Ubicación:** `myapp/views.py` contact_view

**Riesgo:**
- Spam masivo
- Abuso de recursos
- Ataques de negación de servicio (DoS)

**Impacto:** 🔴 **ALTO** - Disponibilidad

**Solución:**

```bash
pip install django-ratelimit
```

```python
# en views.py
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/h', method='POST')  # 5 contactos/hora por IP
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # ... guardar ...
            return render(request, 'contacto_success.html')
    else:
        form = ContactForm()
    return render(request, 'contacto.html', {'form': form})
```

**O con django-axes (para intentos fallidos):**
```bash
pip install django-axes
```

---

### 7. Sin Validación de ALLOWED_HOSTS

**Ubicación:** `mysite/settings.py` línea 28

```python
# ⚠️ OK PARA DESARROLLO pero insuficiente para producción
ALLOWED_HOSTS = ['192.168.1.73', 'localhost']
```

**Riesgo:** Host Header Injection

**Solución:**

```python
# ✅ PRODUCCIÓN
ALLOWED_HOSTS = [
    'tudominio.com',
    'www.tudominio.com',
    '192.168.1.100',  # IP si es necesaria
]

# Con variables de entorno
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1'
).split(',')
```

---

## 🟡 MEDIAS

### 8. Sin Content Security Policy (CSP)

**Riesgo:** XSS sin restricción de recursos

**Solución:**

```bash
pip install django-csp
```

```python
# settings.py
MIDDLEWARE = [
    'csp.middleware.CSPMiddleware',
    # ... otros middleware ...
]

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "https://cdn.jsdelivr.net")
CSP_STYLE_SRC = ("'self'", "https://fonts.googleapis.com")
CSP_FONT_SRC = ("https://fonts.gstatic.com",)
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)
```

---

### 9. Sin Protección X-Frame-Options

**Ubicación:** settings.py (verificar si está)

```python
# ✅ Agregar si no existe
X_FRAME_OPTIONS = 'DENY'  # Previene clickjacking
```

---

### 10. Sin Logs Estructurados

**Riesgo:** No auditable, difícil depuración

**Solución:**

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

```python
# en views.py
import logging
logger = logging.getLogger('django')

def contact_view(request):
    logger.info(f"Contact form accessed from {request.META.get('REMOTE_ADDR')}")
    # ...
```

---

### 11. Sin Validación de Archivo (si se agrega upload)

**Riesgo (futuro):** Upload de malware

**Solución:**
```python
# forms.py
import os
from django import forms

class ContactForm(forms.Form):
    # ... otros campos ...
    archivo = forms.FileField(required=False)
    
    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            # Validar tamaño
            if archivo.size > 5 * 1024 * 1024:  # 5 MB
                raise forms.ValidationError("Archivo muy grande (máx 5MB)")
            
            # Validar tipo MIME
            allowed_mimes = ['application/pdf', 'image/png', 'image/jpeg']
            if archivo.content_type not in allowed_mimes:
                raise forms.ValidationError("Tipo de archivo no permitido")
        
        return archivo
```

---

## 🟢 BAJAS

### 12. Sin Compresión de Respuestas

**Solución:**

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',  # Comprimir respuestas
    # ... otros middleware ...
]
```

---

### 13. Sin Headers de Seguridad Adicionales

**Solución:**

```python
# settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'",),
    'style-src': ("'self'", "'unsafe-inline'"),  # Si es necesario
}
```

---

### 14. Sin Versionado de Estáticos

**Solución:**

```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
```

---

## ✅ Checklist de Implementación

### Antes de Producción (Crítico)

- [ ] **SECRET_KEY** en variables de entorno
- [ ] **DEBUG = False**
- [ ] **ALLOWED_HOSTS** configurado
- [ ] **HTTPS/TLS** habilitado
- [ ] **Base de datos PostgreSQL** (no SQLite)
- [ ] **SECURE_SSL_REDIRECT = True**
- [ ] **SESSION_COOKIE_SECURE = True**
- [ ] **CSRF_COOKIE_SECURE = True**
- [ ] **Ejecutar:** `python manage.py check --deploy`

### Nivel Medio (Importante)

- [ ] Rate limiting en formulario
- [ ] Content Security Policy (CSP)
- [ ] Sanitización de entrada (bleach)
- [ ] Logging estructurado
- [ ] Monitoreo de errores (Sentry)
- [ ] Backup automático de BD
- [ ] Compresión GZIP habilitada

### Nice to Have (Mejora)

- [ ] CAPTCHA en formulario
- [ ] 2FA para admin
- [ ] Versionado de estáticos
- [ ] CDN para assets
- [ ] Métricas y APM
- [ ] Tests de seguridad automatizados

---

## 🔍 Comandos de Verificación

```bash
# Validar configuración de seguridad
python manage.py check --deploy

# Ver headers de seguridad
curl -I https://tudominio.com

# Analizar dependencias vulnerables
pip install safety
safety check

# O con pip-audit
pip install pip-audit
pip-audit

# Verificar SSL/TLS
openssl s_client -connect tudominio.com:443 -showcerts
```

---

## 📚 Referencias

- [Django Security Documentation](https://docs.djangoproject.com/en/5.0/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Security.txt](https://securitytxt.org/)
- [Mozilla Observatory](https://observatory.mozilla.org/)

---

## 🎓 Resumen

**Vulnerabilidades encontradas:** 11 (3 críticas, 4 altas, 4 medias)

**Esfuerzo de remediación:**
- Críticas: 2-4 horas
- Altas: 4-8 horas
- Totales: ~1-2 días de trabajo

**Recomendación:** ⛔ NO desplegar en producción sin hacer al menos los cambios CRÍTICOS.
