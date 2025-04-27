# StackcloneBackend

StackcloneBackend es un proyecto basado en Django que replica funcionalidades básicas de una plataforma de preguntas y respuestas similar a Stack Overflow. Este backend incluye autenticación, gestión de usuarios, preguntas, respuestas, artículos, logros y más.

## Características principales

- **Autenticación JWT**: Implementada con `rest_framework_simplejwt` y `djoser`.
- **Gestión de usuarios**: Personalización del modelo de usuario (`CustomUser`) y endpoints para registro, inicio de sesión, recuperación de contraseñas, etc.
- **Gestión de contenido**: Soporte para preguntas, respuestas, artículos y logros.
- **Paginación**: Configuración predeterminada con `PageNumberPagination`.
- **Admin personalizado**: Interfaz de administración mejorada con `django-jazzmin`.

## Requisitos previos

- Python 3.10 o superior
- Django 5.2
- Virtualenv (opcional, pero recomendado)

## Instalación

1. Clona este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd StackcloneBackend
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Realiza las migraciones de la base de datos:
   ```bash
   python manage.py migrate
   ```

5. Inicia el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

## Endpoints principales

### Autenticación
- `/api/auth/jwt/create/`: Obtener un token de acceso.
- `/api/auth/jwt/refresh/`: Refrescar el token de acceso.
- `/api/auth/jwt/verify/`: Verificar la validez del token.

### Usuarios
- `/api/auth/users/`: Gestión de usuarios (registro, detalles, etc.).
- `/api/auth/users/me/`: Información del usuario autenticado.

### Preguntas y Respuestas
- `/api/questions/questions/`: Listar y crear preguntas.
- `/api/questions/answers/`: Listar y crear respuestas.

### Artículos
- `/api/articles/articles/`: Listar y gestionar artículos.

### Logros
- `/api/achievements/achievements/`: Listar y gestionar logros.

## Configuración adicional

### Variables de entorno
Asegúrate de configurar las siguientes variables de entorno en producción:
- `SECRET_KEY`: Clave secreta de Django.
- `DEBUG`: Establecer en `False` en producción.
- `ALLOWED_HOSTS`: Lista de dominios permitidos.

### Archivos estáticos
Ejecuta el siguiente comando para recopilar los archivos estáticos:
```bash
python manage.py collectstatic
```

## Tecnologías utilizadas

- **Framework**: Django, Django REST Framework
- **Autenticación**: Simple JWT, Djoser
- **Base de datos**: SQLite (por defecto, puedes cambiarla en `settings.py`)
- **Admin**: Django Jazzmin


### Gestión de Artículos

El módulo de artículos permite a los usuarios crear, leer, actualizar y eliminar artículos. Además, incluye funcionalidades para auditar cambios y gestionar estados de los artículos.

#### Endpoints relacionados

- **Artículos**:
  - `GET /api/articles/articles/`: Lista todos los artículos.
  - `POST /api/articles/articles/`: Crea un nuevo artículo.
  - `GET /api/articles/articles/<id>/`: Obtiene los detalles de un artículo específico.
  - `PUT /api/articles/articles/<id>/`: Actualiza un artículo existente.
  - `DELETE /api/articles/articles/<id>/`: Elimina un artículo.

- **Auditoría de Artículos**:
  - `GET /api/articles/article-audits/`: Lista los registros de auditoría de artículos.
  - `GET /api/articles/article-audits/<id>/`: Obtiene los detalles de un registro de auditoría específico.

- **Estados de Artículos**:
  - `GET /api/articles/status/`: Lista los estados disponibles para los artículos.
  - `POST /api/articles/status/`: Crea un nuevo estado.
  - `GET /api/articles/status/<id>/`: Obtiene los detalles de un estado específico.
  - `PUT /api/articles/status/<id>/`: Actualiza un estado existente.
  - `DELETE /api/articles/status/<id>/`: Elimina un estado.

#### Funcionalidades principales

- **Creación y edición**: Los usuarios autenticados pueden crear y modificar artículos.
- **Auditoría**: Cada cambio realizado en un artículo se registra para mantener un historial detallado.
- **Gestión de estados**: Los artículos pueden tener estados personalizados, como "Borrador", "Publicado", o "Archivado".

#### Ejemplo de solicitud para crear un artículo

```bash
curl -X POST http://localhost:8000/api/articles/articles/ \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{
  "title": "Mi primer artículo",
  "content": "Este es el contenido del artículo.",
  "status": 1
}'
```


## Licencia

Este proyecto está bajo la licencia MIT.
