AMERICAN SCHOOL WAY — CAMPAÑA NOVIEMBRE 2026
VERSIÓN PREPARADA PARA RAILWAY Y ACCESO WEB EN CALI
==================================================

QUÉ PERMITE
-----------
- Acceso desde cualquier conexión a Internet, no solo desde la red local.
- Una aplicación compartida para Cali Norte, Cali San Fernando y Cali Limonar.
- PostgreSQL centralizado para que todas las sedes trabajen sobre los mismos registros.
- Inicio de sesión y permisos por sede; administrador con vista general.
- Fechas de matrícula: 1 al 30 de noviembre de 2026.
- Imagen suministrada por el usuario incluida en static/images/.
- Endpoint de comprobación: /healthz.

IMPORTANTE ANTES DE USAR CON MATRÍCULAS REALES
----------------------------------------------
1. La base nueva queda vacía. No se insertan automáticamente los 80 registros
   ficticios que se utilizaban como datos de demostración.
2. Railway debe tener un servicio PostgreSQL persistente y DATABASE_URL conectado.
   No uses SQLite para producción.
3. Configura contraseñas fuertes y distintas para los cuatro usuarios.
4. Los datos personales son privados. Comparte la URL solo con personal autorizado.
5. Antes de uso institucional definitivo, realiza pruebas, copias de seguridad y
   revisión de privacidad/seguridad con el responsable de la organización.

PUBLICACIÓN EN RAILWAY
----------------------
PASO 1 — GitHub
1. Entra a https://railway.com/ y crea/inicia sesión.
2. Sube el contenido de esta carpeta a un repositorio PRIVADO de GitHub.
   railway.toml debe quedar en la raíz del repositorio.
3. No subas .env, contraseñas ni datos reales de estudiantes.

PASO 2 — PostgreSQL y aplicación
1. En Railway crea un Project.
2. Añade un servicio PostgreSQL (New → Database → PostgreSQL).
3. Añade un servicio desde GitHub Repo y selecciona el repositorio.
4. En Variables del servicio de la aplicación configura:
   DATABASE_URL = ${{Postgres.DATABASE_URL}}
   (Si tu servicio PostgreSQL tiene otro nombre, usa ese nombre exacto.)
   SECRET_KEY = una cadena aleatoria larga y privada
   COOKIE_SECURE = true
   ADMIN_PASSWORD = contraseña fuerte exclusiva del administrador
   NORTE_PASSWORD = contraseña fuerte para sede Norte
   SAN_FERNANDO_PASSWORD = contraseña fuerte para San Fernando
   LIMONAR_PASSWORD = contraseña fuerte para Limonar
   LOAD_DEMO_DATA = false

PASO 3 — Desplegar
1. Railway detecta Python y requirements.txt.
2. railway.toml y Procfile definen el comando de inicio.
3. Espera a que termine el despliegue.
4. En Settings → Networking, genera un dominio público (Generate Domain).
5. Abre la URL HTTPS y prueba el acceso de cada sede.

USUARIOS
--------
admin          Acceso administrativo a todas las sedes.
NORTE          Solo Cali Norte.
SAN_FERNANDO   Solo Cali San Fernando.
LIMONAR        Solo Cali Limonar.
Las contraseñas no vienen incluidas en el ZIP; se establecen en Railway Variables.
La primera inicialización crea los usuarios si aún no existen.

PRUEBAS ANTES DE COMPARTIR
--------------------------
- Abrir /healthz y confirmar {"status":"ok"}.
- Iniciar sesión como administrador y como cada sede.
- Comprobar que cada sede solo ve sus propios registros.
- Crear, editar y eliminar un registro de prueba.
- Confirmar que los cambios se ven desde otro dispositivo.
- Borrar los registros de prueba antes de abrir el sistema al personal.

EJECUCIÓN LOCAL
---------------
Instala Python 3.11+, ejecuta:
  py -m venv .venv
  .venv\Scripts\activate
  pip install -r requirements.txt
  python app.py
Abre http://127.0.0.1:5000
Para pruebas locales se permite SQLite. Nunca reutilices contraseñas de desarrollo
para el entorno público.
