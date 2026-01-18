# Backend Stack Develop 🚀

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/) [![Django](https://img.shields.io/badge/Django-4.x-green.svg)](https://www.djangoproject.com/) [![Django REST Framework](https://img.shields.io/badge/DRF-3.x-red.svg)](https://www.django-rest-framework.org/)

## Descripción del Proyecto 📝

Este repositorio aloja el backend de un clon mejorado de Stack Overflow, diseñado para ser una plataforma robusta de preguntas y respuestas. Desarrollado con **Django** y **Django REST Framework**, el proyecto se enfoca en proporcionar una API escalable y segura. Incluye funcionalidades esenciales como la gestión de usuarios, artículos, preguntas, respuestas, un sistema de votación, gamificación con puntos y logros, y una interfaz de administración mejorada con `Unfold`. La autenticación se gestiona de forma segura mediante **JSON Web Tokens (JWT)** basados en cookies, ofreciendo una base sólida para aplicaciones web o móviles interactivas.

## Características Principales ✨

*   **Arquitectura Modular**: Organizado en aplicaciones Django (`achievements`, `articles`, `points`, `questions`, `tags`, `users`, `votes`) para facilitar la gestión, el desarrollo y la escalabilidad.
*   **Autenticación Segura con JWT**: Implementa un sistema de autenticación moderno y seguro usando JSON Web Tokens, gestionados a través de cookies para una mejor experiencia de usuario y seguridad.
*   **Experiencia de Administración Mejorada**: Utiliza `Unfold` para personalizar y modernizar la interfaz de administración de Django, ofreciendo una experiencia más intuitiva y agradable.
*   **Funcionalidades Centrales de Q&A**: Incluye módulos para la gestión de preguntas, respuestas, comentarios y etiquetas, replicando las características esenciales de una plataforma como Stack Overflow.
*   **Sistema de Gamificación**: Incorpora sistemas de puntos y logros para incentivar la participación y recompensar a los usuarios activos.
*   **API RESTful Completa**: Expone todas las funcionalidades a través de una API RESTful bien definida, lo que permite una fácil integración con diversos clientes frontend (web, móvil).
*   **Gestión de Contenido**: Capacidades para crear, leer, actualizar y eliminar artículos y contenido generado por el usuario.
*   **Pruebas Integradas**: La presencia de directorios `test/` dentro de cada aplicación sugiere un enfoque en la calidad del código y la robustez de las funcionalidades.

## Requisitos Previos 🛠️

Antes de comenzar, asegúrate de tener instalado lo siguiente:

*   [Python](https://www.python.org/downloads/) 3.9 o superior
*   `pip` (administrador de paquetes de Python)
*   Una base de datos compatible con Django (se recomienda PostgreSQL para producción, pero SQLite es suficiente para desarrollo).

## Instrucciones de Instalación 🚀

Sigue estos pasos para configurar y ejecutar el proyecto localmente:

1.  **Clonar el repositorio**:
    ```bash
    git clone https://github.com/alejav0240/Stack-Clone-Backend.git
    cd Stack-Clone-Backend
    ```

2.  **Crear y activar un entorno virtual**:
    Es una buena práctica usar entornos virtuales para gestionar las dependencias del proyecto.
    ```bash
    python -m venv venv
    # En Windows
    .\venv\Scripts\activate
    # En macOS/Linux
    source venv/bin/activate
    ```

3.  **Instalar las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno**:
    Crea un archivo `.env` en el directorio raíz del proyecto (junto a `manage.py`) y añade tus configuraciones. Puedes usar `.env.example` como plantilla. Por ejemplo:
    ```
    SECRET_KEY='tu_clave_secreta_de_django_muy_segura'
    DEBUG=True
    DATABASE_URL='sqlite:///db.sqlite3' # O tu URL de PostgreSQL/MySQL, e.g., 'postgresql://user:password@host:port/database_name'
    # JWT Settings
    ACCESS_TOKEN_LIFETIME_MINUTES=5
    REFRESH_TOKEN_LIFETIME_DAYS=1
    ```
    Asegúrate de reemplazar `tu_clave_secreta_de_django_muy_segura` con una clave secreta fuerte y la `DATABASE_URL` con la configuración de tu base de datos.

5.  **Realizar migraciones de la base de datos**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Crear un superusuario (opcional, para acceder al panel de administración)**:
    ```bash
    python manage.py createsuperuser
    ```

7.  **Ejecutar el servidor de desarrollo**:
    ```bash
    python manage.py runserver
    ```
    El backend estará disponible en `http://127.0.0.1:8000/`. El panel de administración estará en `http://127.0.0.1:8000/admin/`.

## Guía de Uso (Ejemplos de Endpoints de API) 💡

Aquí tienes algunos ejemplos de los endpoints de la API que puedes esperar. Para detalles completos, se recomienda explorar la documentación de la API (si está disponible a través de `drf-yasg` o `drf-spectacular`) o el código fuente.

**Autenticación:**

*   **Registro de Usuario**: `POST /api/users/register/`
    ```json
    {
        "email": "nuevo@ejemplo.com",
        "password": "una_contraseña_segura",
        "name": "Nuevo",
        "lastname": "Usuario"
    }
    ```
*   **Inicio de Sesión (Obtener Tokens)**: `POST /api/users/login/`
    ```json
    {
        "email": "usuario@ejemplo.com",
        "password": "tu_contraseña"
    }
    ```
*   **Refrescar Token**: `POST /api/users/token/refresh/` (usando el refresh token en cookies)
*   **Cerrar Sesión**: `POST /api/users/logout/`

**Preguntas:**

*   **Listar Preguntas**: `GET /api/questions/`
*   **Crear Pregunta**: `POST /api/questions/` (requiere autenticación)
*   **Ver Detalle de Pregunta**: `GET /api/questions/{id}/`
*   **Votar Pregunta**: `POST /api/questions/{id}/vote/` (requiere autenticación)

**Usuarios:**

*   **Ver Perfil del Usuario Actual**: `GET /api/users/me/` (requiere autenticación)

## Estructura del Proyecto 🌳
```
Stack-Clone-Backend/
├── StackcloneBackend/          # Configuración principal del proyecto Django
│   ├── settings.py             # Configuración del proyecto
│   ├── urls.py                 # URL's globales del proyecto
│   └── ...
├── achievements/               # Gestión de logros de usuario
│   ├── models.py
│   ├── views.py
│   └── ...
├── articles/                   # Gestión de artículos y publicaciones
│   ├── models.py
│   ├── views.py
│   └── ...
├── points/                     # Sistema de puntos para usuarios
│   ├── models.py
│   ├── views.py
│   └── ...
├── questions/                  # Core de preguntas, respuestas y comentarios
│   ├── models.py
│   ├── views.py
│   └── ...
├── tags/                       # Gestión de etiquetas para preguntas y artículos
│   ├── models.py
│   ├── views.py
│   └── ...
├── users/                      # Gestión de usuarios, autenticación y perfiles
│   ├── models.py
│   ├── views.py
│   ├── authentication.py       # Lógica de autenticación JWT
│   └── ...
├── votes/                      # Sistema de votación para contenido
│   ├── models.py
│   ├── views.py
│   └── ...
├── .env.example                # Ejemplo de archivo de variables de entorno
├── LICENSE                     # Información de la licencia
├── README.md                   # Este archivo
├── ddl.dbml                    # Definición del esquema de la base de datos (DBML)
├── ddl.sql                     # Script SQL para la base de datos
├── diagramDatabase.png         # Diagrama visual de la base de datos
├── manage.py                   # Utilidad de línea de comandos de Django
└── requirements.txt            # Dependencias del proyecto
```

## Tecnologías Utilizadas 💻

*   **Python**: Lenguaje de programación principal.
*   **Django**: Framework web de alto nivel para un desarrollo rápido y limpio.
*   **Django REST Framework**: Toolkit flexible para construir APIs web robustas.
*   **djangorestframework-simplejwt**: Implementación sencilla y segura de JWT para DRF.
*   **django-unfold**: Tema moderno y personalizable para el panel de administración de Django.
*   **python-dotenv**: Gestión de variables de entorno desde archivos `.env`.