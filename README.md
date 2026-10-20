# Campus Biblioteca API
Actividad 6. Django, DRF, Swagger, usuario con email y matricula, CRUD administrativo y JWT.

## Instalacion en Windows
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py test
python manage.py runserver 127.0.0.1:8016
```
Swagger: http://127.0.0.1:8016/swagger/
Admin: http://127.0.0.1:8016/admin/

POST /api/v1/auth/token/ recibe email y password. En Authorize de Swagger escribir `Bearer <access>`.
GET /api/v1/auth/me/ requiere JWT. CRUD /api/v1/users/ solo para personal administrador.
Tokens: acceso 15 minutos, refresh 1 dia.

`password` es write_only. create_user y set_password generan el hash. PUT/PATCH sin password conservan el hash original del usuario editado. Password vacio es rechazado.
El campo matricula es unico y aparece en el admin y esquema Swagger.
SQLite se usa para esta practica siguiendo el manual. No se incluye la base, el entorno ni la clave local en Git.
Configuracion local de desarrollo: para desplegar establecer DJANGO_DEBUG=0 y DJANGO_SECRET_KEY y configurar HTTPS y hosts.

Con el entorno instalado, ejecutar INICIAR.ps1 desde la carpeta del proyecto.
