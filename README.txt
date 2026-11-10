AMERICAN SCHOOL WAY — SISTEMA WEB DE MATRÍCULAS
Tema visual: oscuro / neón · Campaña: noviembre de 2026

CAMBIOS DE ESTA VERSIÓN
-----------------------
- Interfaz oscura con acentos neón cian, violeta y magenta.
- Fondo de noviembre oscurecido para mejorar la legibilidad.
- Incluye 95 registros de demostración con el prefijo [DEMO].
- Capacidad total: 100 cupos. Si la base de datos está vacía y se activa la
  carga inicial, se mostrarán exactamente 5 cupos disponibles.
- Los registros ficticios se cargan solo una vez y solo si la tabla está vacía.

ATENCIÓN: DATOS DE DEMOSTRACIÓN
-------------------------------
Los 95 registros [DEMO] son completamente artificiales y sirven únicamente
para revisar la apariencia y las funciones del sistema. No son estudiantes
reales, no representan matrículas confirmadas y deben eliminarse antes de
usar el sistema para registrar personas reales. No mezcles registros DEMO
con matrículas reales.

ACTUALIZAR EL PROYECTO EN GITHUB Y RENDER
----------------------------------------
1. Descomprime este ZIP.
2. En GitHub abre el repositorio ASW y selecciona Add file > Upload files.
3. Sube el contenido de la carpeta del proyecto, reemplazando los archivos
   existentes. Asegúrate de conservar app.py, render.yaml, Procfile,
   requirements.txt y las carpetas templates/ y static/ en la raíz.
4. Confirma los cambios (Commit changes).
5. Render detectará el commit y desplegará la nueva versión.

CARGA ÚNICA DE LOS 95 REGISTROS DE DEMOSTRACIÓN
------------------------------------------------
IMPORTANTE: haz esto solamente si todavía no existen matrículas reales en la
base de datos. El programa NO agrega ni reemplaza registros si ya hay al menos
una fila en la tabla people.

1. En Render abre el servicio american-school-way-matriculas.
2. Entra a Environment.
3. Busca SEED_DEMO_DATA y cambia su valor de false a true.
4. Guarda y espera a que el servicio termine el nuevo deploy.
5. Abre la página: deben aparecer 95 registros [DEMO] y 5 cupos disponibles.
6. Regresa a Environment y cambia SEED_DEMO_DATA a false.
7. Guarda y espera el siguiente deploy. Los registros permanecerán en PostgreSQL;
   cambiar la variable a false evita que se intente cargar la demostración otra vez.

NO actives SEED_DEMO_DATA si ya hay matrículas reales. La carga solo funciona
cuando la tabla está vacía y no elimina datos existentes.

ACCESOS
-------
- admin: administrador con acceso a todas las sedes.
- NORTE: Cali Norte.
- SAN_FERNANDO: Cali San Fernando.
- LIMONAR: Cali Limonar.
Las contraseñas se configuran en las variables privadas de Render. Nunca las
subas a GitHub ni las compartas públicamente.

ANTES DE OPERAR CON ESTUDIANTES REALES
--------------------------------------
Elimina los registros [DEMO] desde la cuenta administradora y verifica que el
contador de cupos sea correcto. Revisa la política de tratamiento de datos,
permisos, copias de seguridad y plan de PostgreSQL. No uses una base gratuita
con vencimiento para datos reales de matrícula.
