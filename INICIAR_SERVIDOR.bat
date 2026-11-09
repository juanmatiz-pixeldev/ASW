@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================
echo   AMERICAN SCHOOL WAY - CAMPAÑA NOVIEMBRE 2026
echo ============================================================
where python >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python no esta instalado o no esta en PATH.
  pause
  exit /b 1
)
if not exist .venv (
  echo Creando entorno virtual...
  python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
if not defined ADMIN_PASSWORD (
  echo.
  echo Faltan variables de contrasena. Consulte README.txt y configure
  echo ADMIN_PASSWORD, NORTE_PASSWORD, SAN_FERNANDO_PASSWORD y LIMONAR_PASSWORD
  echo en PowerShell antes de iniciar la aplicacion.
  pause
  exit /b 1
)
if not defined NORTE_PASSWORD goto missing
if not defined SAN_FERNANDO_PASSWORD goto missing
if not defined LIMONAR_PASSWORD goto missing
if not defined SECRET_KEY set SECRET_KEY=clave-local-debe-cambiarse-antes-de-produccion

echo.
echo Servidor iniciado en http://127.0.0.1:5000
echo Para detenerlo, cierre esta ventana.
python app.py
pause
:missing
echo Faltan una o mas contrasenas. Consulte README.txt.
pause
