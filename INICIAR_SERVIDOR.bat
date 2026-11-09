@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================
echo   AMERICAN SCHOOL WAY - SERVIDOR DE MATRICULAS
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
for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr /R /C:"IPv4.*:"') do set IP=%%A
set IP=%IP: =%
echo.
echo Servidor iniciado.
echo En este PC:  http://127.0.0.1:5000
if defined IP echo En la red:   http://%IP%:5000
 echo.
echo Mantenga esta ventana abierta mientras use la aplicacion.
echo Para detener el servidor, cierre esta ventana.
 echo.
python app.py
pause
