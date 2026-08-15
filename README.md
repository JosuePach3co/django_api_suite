# Django API Suite

Backend desarrollado con Django y Django REST Framework (DRF) que actúa como intermediario entre las aplicaciones cliente y una base de datos Firebase Realtime Database, garantizando seguridad, rendimiento y extensibilidad en la comunicación de datos.

## Objetivo

Desarrollar una aplicación backend robusta y escalable utilizando Django que integre un REST API completo, facilitando la comunicación con las aplicaciones cliente mediante endpoints seguros, eficientes y extensibles.

## Estructura del proyecto
```text
django_api_suite/
├── backend_data_server/        # Configuración principal del proyecto
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── homepage/                   # Aplicación de presentación (SSR)
│   ├── views.py
│   └── urls.py
├── demo_rest_api/              # API REST demo con CRUD en memoria
│   ├── views.py
│   └── urls.py
├── landing_api/                # API REST conectada a Firebase Realtime Database
│   ├── views.py
│   ├── urls.py
│   └── apps.py
├── templates/homepage/         # Plantillas HTML
├── static/img/                 # Archivos estáticos
├── secrets/                    # Clave privada de Firebase (no versionado)
├── requirements.txt
└── manage.py
```

## Aplicaciones

### 1. `homepage`
Vista basada en funciones que renderiza una plantilla HTML mediante Server Side Rendering (SSR).

- **Ruta:** `/homepage/index/`
- **Método:** `GET`

### 2. `demo_rest_api`
API REST de demostración con operaciones CRUD completas sobre datos almacenados en memoria (lista Python).

- **Ruta base:** `/demo/rest/api/index/`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/demo/rest/api/index/` | Lista los elementos activos |
| `POST` | `/demo/rest/api/index/` | Crea un nuevo elemento (requiere `name` y `email`) |
| `PUT` | `/demo/rest/api/index/<id>/` | Reemplaza completamente un elemento |
| `PATCH` | `/demo/rest/api/index/<id>/` | Actualiza parcialmente un elemento |
| `DELETE` | `/demo/rest/api/index/<id>/` | Elimina lógicamente un elemento (`is_active = False`) |

### 3. `landing_api`
API REST conectada a Firebase Realtime Database mediante Firebase Admin Python SDK, para persistencia real de datos.

- **Ruta base:** `/landing/api/index/`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/landing/api/index/` | Obtiene todos los registros de la colección `landing_entries` |
| `POST` | `/landing/api/index/` | Crea un nuevo registro con timestamp automático (formato `dd/mm/yyyy, hh:mm:ss a. m./p. m.`) |

## Tecnologías utilizadas

- **Django 5.2.8**
- **Django REST Framework 3.18.0**
- **Firebase Admin Python SDK 7.5.0**
- **Python 3.10**
- **Firebase Realtime Database**
- **PythonAnywhere** (hosting/despliegue)

## Configuración local

1. Clonar el repositorio:
```bash
   git clone https://github.com/JosuePach3co/django_api_suite.git
   cd django_api_suite
```

2. Crear y activar el entorno virtual:
```bash
   python -m venv env
   source env/bin/activate
```

3. Instalar dependencias:
```bash
   pip install -r requirements.txt
```

4. Configurar la clave privada de Firebase:
   - Crear la carpeta `secrets/` en la raíz del proyecto.
   - Descargar la clave privada desde Firebase Console → Configuración del proyecto → Cuentas de servicio → SDK de Firebase Admin.
   - Guardarla como `secrets/landing-key.json`.

5. Levantar el servidor de desarrollo:
```bash
   python manage.py runserver
```

## Despliegue

El proyecto está desplegado en PythonAnywhere:

**URL base:** `http://pablochacon.pythonanywhere.com/`

Endpoints disponibles en producción:
- `http://pablochacon.pythonanywhere.com/homepage/index/`
- `http://pablochacon.pythonanywhere.com/demo/rest/api/index/`
- `http://pablochacon.pythonanywhere.com/landing/api/index/`

### Notas de despliegue

- El entorno virtual en PythonAnywhere usa **Python 3.10**, por lo que la versión de Django debe ser compatible (`5.2.8`, ya que Django 6.x requiere Python 3.12+).
- La `databaseURL` en `settings.py` debe coincidir con el `project_id` de la clave privada de Firebase (`secrets/landing-key.json`).
- Tras cualquier cambio en el código, es necesario ejecutar `git pull` en la consola de PythonAnywhere y recargar (**Reload**) la Web App.

## Seguridad

- La clave privada de Firebase (`secrets/landing-key.json`) está excluida del control de versiones mediante `.gitignore`.
- `ALLOWED_HOSTS` está configurado únicamente con el dominio de producción.
- Las operaciones de eliminación en `demo_rest_api` son lógicas (no destructivas), preservando el historial de datos.

## Autores

- Pablo Chacón — [@pablochacon08](https://github.com/pablochacon08)
- Josué Pacheco — [@JosuePach3co](https://github.com/JosuePach3co)