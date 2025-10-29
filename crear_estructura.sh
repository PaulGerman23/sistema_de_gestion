=== file: crear_estructura.sh ===
#!/bin/bash

# Script para crear la estructura de directorios del proyecto

mkdir -p app/routes
mkdir -p app/templates/inventory
mkdir -p app/templates/ventas
mkdir -p app/static/adminlte

# Crear archivos __init__.py vacíos
touch app/__init__.py
touch app/routes/__init__.py

echo "Estructura de directorios creada exitosamente"
echo ""
echo "IMPORTANTE: Descarga AdminLTE desde https://adminlte.io/"
echo "y copia el contenido de la carpeta 'dist/' a 'app/static/adminlte/'"
echo ""
echo "Luego ejecuta:"
echo "  pip install -r requirements.txt"
echo "  python run.py"
