============================================================
 AMERICAN SCHOOL WAY
 SISTEMA DE MATRÍCULAS — CAMPAÑA NOVIEMBRE 2026
 VERSIÓN V5 — CAMPAÑA NOVIEMBRE 2026 / INTERNET / VARIOS COMPUTADORES
============================================================

QUE INCLUYE
-----------
- 100 cupos.
- 80 registros iniciales.
- 19 con estado "Pagó - esperando material".
- 61 con estado "Ya se encuentra matriculado".
- 1 cupo disponible.
- Nombre, ID/cédula, paquete, estado y fecha/hora.
- Paquetes de 1, 3 o 6 niveles.
- Paquete 1: A1.
- Paquete 3: A1, A2, B1.
- Paquete 6: A1, A2, B1, B2, B2+ y Exceptional Level.
- Fechas permitidas: 1 al 30 de noviembre de 2026.
- Edición y eliminación de registros.
- Base de datos PostgreSQL en producción.
- Inicio de sesión para proteger los datos.
- 4 usuarios fijos: admin, NORTE, SAN_FERNANDO y LIMONAR.
- admin tiene acceso a todas las sedes y es la única cuenta administrativa.
- NORTE solo trabaja con Cali Norte.
- SAN_FERNANDO solo trabaja con Cali San Fernando.
- LIMONAR solo trabaja con Cali Limonar.
- Una matrícula queda en la sede del usuario que la registra; NO se asigna aleatoriamente.
- Solo admin puede cambiar la sede de una matrícula al editarla.
- Cada usuario puede cambiar su propia contraseña; admin puede configurar las cuatro.
- Endpoint /healthz para comprobar el servidor.
- Configuración de despliegue para Render mediante render.yaml.
- Encabezado basado en la versión V1, con logo pequeño a la izquierda y nombre centrado visualmente.
- Indicador de cupos disponibles grande, llamativo y parpadeante.
- La imagen de campaña suministrada está en static/images/asw-noviembre-2026.jpeg y se utiliza en el encabezado y en el inicio de sesión.

IMPORTANTE SOBRE LOS DATOS
--------------------------
La versión de Internet NO usa data.json. Usa PostgreSQL para que varios
computadores puedan trabajar al mismo tiempo sobre los mismos registros.

PRUEBA LOCAL
------------
1. Instala Python 3.11+.
2. Abre CMD en esta carpeta.
3. Ejecuta:
       py -m venv .venv
       .venv\Scripts\activate
       pip install -r requirements.txt
4. Define las credenciales de prueba (PowerShell):
       $env:ADMIN_PASSWORD="TU_CLAVE_ADMIN"
       $env:NORTE_PASSWORD="TU_CLAVE_NORTE"
       $env:SAN_FERNANDO_PASSWORD="TU_CLAVE_SAN_FERNANDO"
       $env:LIMONAR_PASSWORD="TU_CLAVE_LIMONAR"
5. Ejecuta:
       python app.py
6. Abre:
       http://127.0.0.1:5000

DEPLOY EN INTERNET CON RENDER
-----------------------------
Esta carpeta incluye render.yaml. Render puede crear el servicio web y la
base de datos PostgreSQL como un Blueprint. El servicio queda accesible por
una URL HTTPS de Render, por ejemplo:
       https://american-school-way-matriculas.onrender.com

PASO 1 — CREAR CUENTA
---------------------
1. Entra a https://render.com/
2. Crea una cuenta.
3. Conecta GitHub.

PASO 2 — SUBIR EL PROYECTO A GITHUB
------------------------------------
1. Crea un repositorio nuevo en GitHub, por ejemplo:
       american-school-way-matriculas
2. Sube TODOS los archivos de esta carpeta al repositorio.
3. render.yaml debe quedar en la raíz del repositorio.

PASO 3 — CREAR EL BLUEPRINT
----------------------------
1. En Render Dashboard selecciona New > Blueprint.
2. Selecciona el repositorio de GitHub.
3. Render detectará render.yaml.
4. Cuando solicite las cuatro contraseñas, configura una contraseña fuerte
   diferente para cada usuario y NO las publiques en GitHub.
5. Aplica el Blueprint.

El Blueprint crea:
- un Web Service Flask/Gunicorn
- una base de datos PostgreSQL
- DATABASE_URL conectado automáticamente
- SECRET_KEY generada automáticamente
- HTTPS del servicio web

PASO 4 — ENTRAR AL SISTEMA
---------------------------
Cuando el deploy termine, Render mostrará la URL pública del servicio.
Abre esa URL desde cualquier computador o celular con Internet, incluido
cualquier lugar de Cali.

Ejemplo:
       https://american-school-way-matriculas.onrender.com

Luego inicia sesión con el usuario `admin` y la contraseña que configuraste
para ADMIN_PASSWORD. Las otras cuentas son `NORTE`, `SAN_FERNANDO` y `LIMONAR`.

SEGURIDAD
---------
- Usa una contraseña fuerte y diferente para cada una de las cuatro cuentas.
- No subas contraseñas a GitHub.
- El usuario `admin` es la única cuenta con acceso administrativo y a todas las sedes.
- No compartas públicamente los números de identificación.
- Mantén el acceso limitado al personal autorizado.
- Para uso continuo después de la campaña, usa un plan de base de datos
  con persistencia/soporte adecuado. En Render, la base de datos gratuita
  tiene limitaciones y expira después de 30 días según la documentación
  actual de Render.

ACTUALIZACIONES
---------------
Cuando cambies el código y hagas push a la rama conectada, Render puede
volver a desplegar automáticamente el servicio.

SI QUIERES USAR DOMINIO PROPIO
------------------------------
Después de tener la aplicación funcionando, desde Render puedes configurar
un dominio propio. Por ejemplo:
       matriculas.tudominio.com

NO NECESITAS
------------
- Que todos los computadores estén en la misma Wi-Fi.
- Que el computador de Cali permanezca encendido.
- Abrir el puerto 5000 del router.
- Configurar port forwarding.

Los usuarios se conectan al servidor en Internet.


Actualización V5: código promocional automático de 6 dígitos, identificación (cédula) separada de 6 a 10 dígitos y datos iniciales aleatorizados.

V12: Campaña actualizada a noviembre de 2026. Se incluye la imagen suministrada por el usuario en static/images/asw-noviembre-2026.jpeg y se utiliza en el encabezado y en el inicio de sesión.

ACTUALIZACIÓN NOVIEMBRE 2026
----------------------------
- Campaña y validación de fechas configuradas del 1 al 30 de noviembre de 2026.
- Fecha predeterminada del formulario: 30 de noviembre de 2026.
- Imagen suministrada por el usuario incluida en static/images/asw-noviembre-2026.jpeg.
- La imagen se muestra en el encabezado principal y en la pantalla de inicio de sesión.
