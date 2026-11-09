AMERICAN SCHOOL WAY — SISTEMA WEB DE MATRÍCULAS
Campaña: noviembre de 2026

OBJETIVO
--------
Esta aplicación Flask está preparada para publicarse en Internet. Una vez
realizado el despliegue, el personal autorizado de las sedes de Cali podrá
entrar desde computadores, tabletas o celulares con conexión a Internet.
Todos los usuarios trabajan contra una única base de datos PostgreSQL.

IMPORTANTE: LA APLICACIÓN NO ESTÁ PUBLICADA TODAVÍA
--------------------------------------------------
El ZIP contiene el código y la configuración de despliegue, pero no crea por
sí solo una dirección pública. Para publicarla se necesita una cuenta de
hosting, una cuenta de GitHub y configurar las contraseñas privadas. La URL
pública se obtiene al completar el despliegue en Render.

ACCESO Y PERMISOS
-----------------
- admin: administrador con acceso a todas las sedes.
- NORTE: solo puede consultar y gestionar matrículas de Cali Norte.
- SAN_FERNANDO: solo puede consultar y gestionar matrículas de Cali San Fernando.
- LIMONAR: solo puede consultar y gestionar matrículas de Cali Limonar.
- Los datos de matrículas NO son públicos. Solo el personal autorizado debe
  recibir las credenciales de acceso.
- Cada sede trabaja sobre la misma base de datos centralizada.

CAMPAÑA NOVIEMBRE 2026
---------------------
- Fechas permitidas: 1 al 30 de noviembre de 2026.
- Capacidad configurada: 100 cupos.
- La imagen enviada para noviembre está incluida en static/images/ y se usa
  tanto en el encabezado como en la pantalla de inicio de sesión.
- No se crean matrículas ficticias automáticamente. La base de datos nueva
  inicia vacía para no mezclar registros de demostración con datos reales.

PUBLICACIÓN EN INTERNET CON RENDER
----------------------------------
1. Crea una cuenta en https://github.com/ y otra en https://render.com/.
2. Descomprime el ZIP y crea un repositorio privado en GitHub.
3. Sube el contenido de la carpeta AMERICAN_SCHOOL_WAY-main al repositorio.
   Verifica que render.yaml quede en la raíz del repositorio.
4. En Render selecciona New > Blueprint y conecta ese repositorio.
5. Render leerá render.yaml y propondrá crear el servicio web y PostgreSQL.
6. Antes de confirmar, revisa los recursos y sus costos. El archivo viene con
   planes gratuitos para pruebas; NO uses los planes gratuitos para operar
   matrículas reales de forma continua.
7. Configura estas cuatro variables secretas cuando Render las solicite:
   ADMIN_PASSWORD
   NORTE_PASSWORD
   SAN_FERNANDO_PASSWORD
   LIMONAR_PASSWORD
   Usa contraseñas diferentes, robustas y de al menos 8 caracteres. No las
   escribas en el código ni las subas a GitHub.
8. Aplica el Blueprint y espera a que el servicio termine el despliegue.
9. Abre la URL HTTPS que Render asigne y prueba cada usuario.
10. Entrega las credenciales únicamente al personal autorizado de cada sede.

PLANES Y CONTINUIDAD
--------------------
Los planes gratuitos de Render son solo para pruebas: el servicio web gratuito
puede suspenderse tras inactividad y la base de datos PostgreSQL gratuita
expira a los 30 días. Render indica que los servicios gratuitos no deben usarse
en producción. Antes de registrar matrículas reales, cambia a un servicio web
pago y una base de datos PostgreSQL paga con persistencia y copias de seguridad.
Consulta los precios vigentes en https://render.com/pricing y las limitaciones
en https://render.com/docs/free.

SEGURIDAD Y DATOS PERSONALES
----------------------------
- Los nombres y números de identificación son datos personales.
- Antes de usar el sistema con estudiantes reales, la empresa debe validar su
  política de tratamiento de datos, autorización de titulares y aviso de
  privacidad conforme a la normativa colombiana aplicable.
- No publiques la URL junto con contraseñas ni compartas usuarios entre sedes.
- Usa contraseñas diferentes y cámbialas desde el sistema cuando corresponda.
- Configura copias de seguridad de PostgreSQL y define quién puede recuperar
  o eliminar información.
- No utilices datos reales en pruebas públicas.

PRUEBA LOCAL (OPCIONAL)
----------------------
Requiere Python 3.11 o superior. En PowerShell, desde esta carpeta:

  py -m venv .venv
  .venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  $env:ADMIN_PASSWORD="una-clave-local-admin"
  $env:NORTE_PASSWORD="una-clave-local-norte"
  $env:SAN_FERNANDO_PASSWORD="una-clave-local-sanfernando"
  $env:LIMONAR_PASSWORD="una-clave-local-limonar"
  $env:SECRET_KEY="una-clave-larga-y-aleatoria-para-pruebas"
  python app.py

Luego abre http://127.0.0.1:5000. Para pruebas con datos ficticios solamente,
puedes establecer antes de iniciar: $env:SEED_DEMO_DATA="true".
No habilites esa variable en producción.

ARCHIVOS PRINCIPALES
--------------------
- app.py: lógica de la aplicación y permisos.
- templates/: páginas web.
- static/images/asw-noviembre-2026.jpeg: imagen de campaña suministrada.
- requirements.txt: dependencias Python.
- render.yaml: configuración del despliegue en Render.
- .gitignore: evita subir bases locales, entornos y archivos secretos.

SALUD DEL SERVICIO
------------------
El endpoint /healthz comprueba que la aplicación puede consultar la base de
datos. Render lo utiliza para verificar el estado del servicio.


PUBLICACIÓN ACTUALIZADA EN RENDER
---------------------------------
- El archivo render.yaml está en la raíz del proyecto y define el Web Service
  Flask/Gunicorn y PostgreSQL como Blueprint.
- Procfile incluido como alternativa para el comando de inicio.
- En Render: New > Blueprint > conecta el repositorio privado de GitHub y
  selecciona este proyecto.
- Revisa el costo y la persistencia de PostgreSQL antes de confirmar. Los
  recursos gratuitos tienen límites y no se recomiendan para matrículas reales.
- Configura ADMIN_PASSWORD, NORTE_PASSWORD, SAN_FERNANDO_PASSWORD y
  LIMONAR_PASSWORD como secretos en Render. No los guardes en GitHub.
- Render genera SECRET_KEY y conecta DATABASE_URL mediante render.yaml.
- Tras el despliegue, comprueba /healthz y prueba los cuatro perfiles.
- La base de datos nueva se inicializa sin matrículas ficticias.
