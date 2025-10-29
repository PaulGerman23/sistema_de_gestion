import os
import sys

def verificar_estructura():
    """
    Verifica que todos los archivos y carpetas necesarios existan
    """
    print("Verificando estructura del proyecto...\n")
    
    archivos_requeridos = [
        'run.py',
        'requirements.txt',
        'app/__init__.py',
        'app/config.py',
        'app/models.py',
        'app/forms.py',
        'app/routes/auth.py',
        'app/routes/dashboard.py',
        'app/routes/inventory.py',
        'app/routes/ventas.py',
        'app/templates/base.html',
        'app/templates/login.html',
        'app/templates/dashboard.html',
        'app/templates/inventory/listar.html',
        'app/templates/inventory/agregar_editar.html',
        'app/templates/ventas/ventas.html',
    ]
    
    carpetas_requeridas = [
        'app',
        'app/routes',
        'app/templates',
        'app/templates/inventory',
        'app/templates/ventas',
        'app/static',
        'app/static/adminlte',
    ]
    
    errores = []
    
    # Verificar carpetas
    print("Verificando carpetas...")
    for carpeta in carpetas_requeridas:
        if os.path.exists(carpeta) and os.path.isdir(carpeta):
            print(f"  ✓ {carpeta}")
        else:
            print(f"  ✗ {carpeta} - FALTA")
            errores.append(f"Carpeta faltante: {carpeta}")
    
    print("\nVerificando archivos...")
    for archivo in archivos_requeridos:
        if os.path.exists(archivo) and os.path.isfile(archivo):
            print(f"  ✓ {archivo}")
        else:
            print(f"  ✗ {archivo} - FALTA")
            errores.append(f"Archivo faltante: {archivo}")
    
    # Verificar AdminLTE
    print("\nVerificando AdminLTE...")
    adminlte_path = 'app/static/adminlte'
    adminlte_archivos = ['css/adminlte.min.css', 'js/adminlte.min.js']
    
    for archivo in adminlte_archivos:
        path_completo = os.path.join(adminlte_path, archivo)
        if os.path.exists(path_completo):
            print(f"  ✓ {archivo}")
        else:
            print(f"  ✗ {archivo} - FALTA")
            errores.append(f"AdminLTE: {archivo} no encontrado")
    
    print("\n" + "="*50)
    if errores:
        print("❌ Verificación FALLIDA")
        print("\nProblemas encontrados:")
        for error in errores:
            print(f"  - {error}")
        print("\nSolución:")
        print("  1. Verifica que todos los archivos estén creados")
        print("  2. Descarga AdminLTE y copia dist/ a app/static/adminlte/")
        return False
    else:
        print("✅ Verificación EXITOSA")
        print("\nEl proyecto está correctamente configurado.")
        print("\nPróximos pasos:")
        print("  1. pip install -r requirements.txt")
        print("  2. python run.py")
        return True

if __name__ == "__main__":
    if verificar_estructura():
        sys.exit(0)
    else:
        sys.exit(1)
