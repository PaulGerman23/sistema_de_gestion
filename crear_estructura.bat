@echo off
REM Script para crear la estructura de directorios del proyecto en Windows

mkdir app\routes
mkdir app\templates\inventory
mkdir app\templates\ventas
mkdir app\static\adminlte

REM Crear archivos __init__.py vacíos
type nul > app\__init__.py
type nul > app\routes\__init__.py

echo Estructura de directorios creada exitosamente
echo.
echo IMPORTANTE: Descarga AdminLTE desde https://adminlte.io/
echo y copia el contenido de la carpeta 'dist/' a 'app/static/adminlte/'
echo.
echo Luego ejecuta:
echo   pip install -r requirements.txt
echo   python run.py
