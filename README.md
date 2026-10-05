# Notificaciones

API para que un usuario autenticado cree, consulte, modifique y borre sus notificaciones. Al crear una, se simula el envío por email, SMS o push.

## Requisitos

- Python 3.12 o superior
- [uv](https://docs.astral.sh/uv/)

## Instalación y ejecución

En la raíz del proyecto:

```powershell
uv sync
copy .env.example .env
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

Antes de arrancar, abre `.env` y reemplaza `SECRET_KEY` por una clave propia de al menos 32 bytes. Esa clave firma los JWT y no se sube al repositorio.

La API queda en `http://127.0.0.1:8000`. La documentación interactiva está en `http://127.0.0.1:8000/docs`.

## Uso

1. `POST /auth/register` con `name`, `email` y `password`.
2. `POST /auth/login` con el mismo email y contraseña. La respuesta trae `access_token`.
3. En el resto de rutas, envía el header `Authorization: Bearer <access_token>`.

Las notificaciones viven en `/notifications`:

| Método | Ruta | Qué hace |
|---|---|---|
| `POST` | `/notifications` | Crea una notificación y la envía por el canal indicado |
| `GET` | `/notifications` | Lista solo las del usuario autenticado |
| `PUT` | `/notifications/{id}` | Modifica una notificación propia |
| `DELETE` | `/notifications/{id}` | Borra una notificación propia |

El cuerpo de alta y de modificación lleva `title`, `content` y `channel` (`email`, `sms` o `push`). Si la notificación no existe o es de otro usuario, la API responde `404`.

## Decisiones técnicas

**FastAPI y SQLAlchemy 2.** Los routers traducen HTTP. Las tablas son modelos de SQLAlchemy y los cuerpos de la API son schemas de Pydantic. SQLite alcanza para ejecutar el proyecto sin un servidor de base de datos aparte. El archivo es `notifications.db`.

**Alembic.** El esquema no se crea al arrancar. Cada cambio de modelo queda en una migración y se aplica con `alembic upgrade head`.

**Autenticación.** La contraseña se guarda con Argon2 (`pwdlib`), nunca en claro. El login devuelve un JWT firmado con `SECRET_KEY`, leída desde el entorno. `get_current_user` valida el token y las rutas de notificaciones lo exigen. Cada fila tiene `user_id`, y las consultas filtran por el usuario del token.

**Canales.** Email, SMS y push implementan el mismo contrato (`send`) y se registran en un diccionario al importar el módulo. El `POST` pide el canal y llama `send`. Agregar un canal nuevo es crear la clase, registrarla e importarla. El endpoint no cambia. El envío es simulado: valida, arma el mensaje y lo deja en el log. No llama a un proveedor real.
