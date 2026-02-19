# Landing Page - Documentación técnica y recomendaciones de seguridad

Resumen
-------
Aplicación Django sencilla que sirve una landing page con varias plantillas, un formulario de contacto, y soporte de temas (light/dark) vía JavaScript y CSS estáticos. Está pensada como proyecto de demostración / micro-site.

Requisitos
----------
- Python 3.8+
- Django (ver `requiriments.txt` en la raíz del proyecto)
- SQLite (el proyecto incluye `db.sqlite3` para desarrollo)

Instalación y ejecución (desarrollo)
----------------------------------
1. Crear y activar un entorno virtual:

```bash
python -m venv .venv
.\.venv\Scripts\activate    # Windows
pip install -r requiriments.txt
```

2. Migraciones y datos iniciales:

```bash
python manage.py migrate
```

3. Ejecutar servidor de desarrollo:

```bash
python manage.py runserver
```

Estructura relevante
--------------------
- `manage.py` - comando de Django.
- `mysite/settings.py` - configuración principal (DEBUG, SECRET_KEY, DATABASES, etc.).
- `myapp/` - aplicación principal que contiene vistas, formularios, modelos y plantillas.
- `myapp/templates/myapp/` - plantillas: `about.html`, `contacto.html`, `hello_world.html`, `legal.html`, `contacto_success.html`, `base.html`.
- `myapp/templates/myapp/static/` - CSS y JS para temas (`dark.css`, `light.css`, `styles.css`, `theme.js`).
- `db.sqlite3` - base de datos SQLite usada en desarrollo.

Memoria técnica
---------------
Arquitectura y stack
- Framework: Django (MVC / MVT).
- Base de datos: SQLite (desarrollo). En producción se recomienda PostgreSQL o MySQL.
- Frontend: plantillas Django + CSS y JS estáticos para cambio de tema.

App `myapp`
- `views.py`: vistas para renderizar las páginas estáticas y procesar el formulario de contacto.
- `forms.py`: formulario `ContactForm` (validación básica con campos requeridos).
- `models.py`: (si existe) modelos para persistencia; en este proyecto la lógica principal es de presentación y formulario.
- `urls.py`: rutas definidas para `about`, `contacto`, `hello_world`, etc.
- Plantillas: `base.html` contiene la estructura común y el cargado del JS de temas.

Flujo del formulario de contacto
- Usuario envía el formulario en `/contacto/`.
- `views.contact` valida `ContactForm`, si es válido muestra `contacto_success.html` y (en configuración real) envía email o guarda el mensaje.

Despliegue
---------
- No usar `DEBUG=True` en producción.
- Configurar `ALLOWED_HOSTS` y una `SECRET_KEY` segura vía variables de entorno.
- Usar un servidor WSGI (Gunicorn/uWSGI) detrás de un proxy (NGINX).
- Usar base de datos robusta (Postgres) y migraciones gestionadas.

Recomendaciones de seguridad (por feature)
-----------------------------------------

General (aplica a todo el proyecto)
- 1) `settings.py`: asegurar `DEBUG=False` en producción y establecer `ALLOWED_HOSTS`.
- 2) Mantener `SECRET_KEY` fuera del repositorio; cargarlo desde variables de entorno.
- 3) Forzar HTTPS a través de proxy y activar `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, y `SECURE_HSTS_SECONDS`.
- 4) Revisar dependencias con `pip-audit` / `safety` y mantener `requiriments.txt` actualizado.
- 5) Activar Content Security Policy (CSP) en cabeceras para mitigar XSS.

Feature: Formulario de contacto (`/contacto/`)
- Riesgos:
  - Inyección de contenido (XSS) si la entrada se renderiza sin escapar.
  - Abuso / spam (envío masivo).
  - Filtración de datos por correo mal configurado.
- Recomendaciones:
  - Validar y sanear entradas en `forms.py`. Usar `clean_` y `strip` para campos de texto.
  - No renderizar contenido de usuario sin escape; usar los mecanismos de plantilla de Django (autoescape).
  - Añadir rate limiting por IP (ej. `django-ratelimit`) y/o CAPTCHA (reCAPTCHA v2/v3) para mitigar spam.
  - Si se envía email, usar `EMAIL_BACKEND` seguro y no exponer credenciales en el repo; usar variables de entorno.
  - Registrar eventos de envío y errores (sin loggear datos sensibles).

Feature: Cambio de tema (JS + CSS)
- Riesgos:
  - Inclusion insegura de recursos externos o ejecución de JS no confiable.
- Recomendaciones:
  - Evitar eval() u operaciones que inyecten HTML desde datos externos.
  - Servir archivos estáticos desde origen controlado; aplicar CSP restringiendo `script-src` y `style-src`.
  - Validar y limitar cualquier dato que se guarde en cookies/localStorage (no guardar tokens sensibles).

Feature: Templates y rendering
- Riesgos:
  - XSS si se usan `|safe` o deshabilita autoescape.
- Recomendaciones:
  - Mantener `autoescape` activo (comportamiento por defecto).
  - Revisar cualquier uso de `|safe` y justificarlo; preferir sanitizar mediante `bleach` si es necesario permitir HTML.

Feature: Admin Django
- Riesgos:
  - Acceso no autorizado al panel admin.
- Recomendaciones:
  - Proteger `/admin/` mediante autenticación fuerte, IP allowlist o VPN para accesos administrativos.
  - Usar contraseñas fuertes y 2FA para cuentas admin.
  - Cambiar la URL por defecto si se desea defensa en profundidad.

Feature: Base de datos (SQLite en desarrollo)
- Riesgos:
  - SQLite no es adecuada para entornos multiusuario y producción a escala.
  - Archivo `db.sqlite3` puede contener datos sensibles.
- Recomendaciones:
  - Para producción usar PostgreSQL o similar.
  - Restringir permisos filesystem al archivo de la base de datos.
  - Hacer backups regulares y cifrarlos si contienen datos sensibles.

Feature: Archivos estáticos y assets
- Riesgos:
  - Exposición de archivos de configuración o rutas internas si la configuración de staticfiles es incorrecta.
- Recomendaciones:
  - Servir estáticos desde un servidor/cdn dedicado (NGINX, CloudFront).
  - Añadir cabeceras de seguridad y cache-control apropiadas.

Auditoría y monitoreo
---------------------
- Habilitar logging estructurado y monitorizar errores (Sentry, Rollbar).
- Revisar logs de acceso y seguridad para detectar intentos de abuso.
- Realizar pruebas periódicas (scans de dependencias, pruebas de penetración básicas).

Checklist rápida antes de producción
-----------------------------------
- [ ] `DEBUG=False` y `ALLOWED_HOSTS` configurado.
- [ ] `SECRET_KEY` en variables de entorno.
- [ ] Certificado TLS y redirección HTTPS.
- [ ] Emails configurados con credenciales seguras.
- [ ] Revisión de dependencias y parches aplicados.
- [ ] Backup y estrategia de migración para BD.

Contribuir y próximos pasos
--------------------------
Proximo Upgrade a generar:
- scripts de despliegue (Gunicorn + NGINX),
- configuración para `docker-compose`,
- o pruebas unitarias para `myapp` — dímelo y las agrego.

Contacto
--------
Para soporte o preguntas: abre un issue en el repo o contáctame directamente.

Licencia
--------
Revisa el repositorio para la licencia aplicable; si no hay, indicar una licencia antes de producción.
