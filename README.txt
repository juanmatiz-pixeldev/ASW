AMERICAN SCHOOL WAY - SISTEMA BLACK NOVEMBER 2026

PROYECTO WEB
- Aplicación Flask con base de datos PostgreSQL.
- Acceso para administración y tres sedes: Cali Norte, Cali San Fernando y Cali Limonar.
- Capacidad total configurada: 100 matrículas.
- Los registros iniciales son información ficticia de muestra y se muestran con nombres normales.
- La imagen de campaña se utiliza exclusivamente en el encabezado del panel.

ACTUALIZACIÓN EN GITHUB Y RENDER
1. Descomprime el ZIP.
2. Sube el contenido a la raíz del repositorio de GitHub, conservando templates/ y static/.
3. Confirma los cambios. Render realizará el despliegue automáticamente.
4. Abre la URL de Render y recarga con Ctrl + F5.

DATOS EXISTENTES
Al iniciar, la aplicación normaliza automáticamente los nombres de registros antiguos que tuvieran un prefijo técnico de muestra. No elimina matrículas ni modifica códigos, identificaciones, sedes, estados o fechas.

SEGURIDAD
No publiques contraseñas ni secretos en GitHub. Mantén las variables ADMIN_PASSWORD, NORTE_PASSWORD, SAN_FERNANDO_PASSWORD y LIMONAR_PASSWORD en el panel Environment de Render.
