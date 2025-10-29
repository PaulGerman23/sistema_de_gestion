import os
import urllib.request
import zipfile
import shutil

def descargar_adminlte():
    """
    Script para descargar y configurar AdminLTE automáticamente
    """
    print("Descargando AdminLTE...")
    
    # URL de descarga de AdminLTE (puedes cambiar a la versión que necesites)
    url = "https://github.com/ColorlibHQ/AdminLTE/archive/refs/heads/master.zip"
    
    # Descargar archivo
    zip_path = "adminlte.zip"
    urllib.request.urlretrieve(url, zip_path)
    
    print("Extrayendo archivos...")
    
    # Extraer zip
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("temp_adminlte")
    
    # Copiar carpeta dist a static
    source_dist = "temp_adminlte/AdminLTE-master/dist"
    target_dir = "app/static/adminlte"
    
    if os.path.exists(source_dist):
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        shutil.copytree(source_dist, target_dir)
        print(f"AdminLTE instalado en {target_dir}")
    else:
        print("No se encontró la carpeta dist en AdminLTE")
    
    # Limpiar archivos temporales
    os.remove(zip_path)
    shutil.rmtree("temp_adminlte")
    
    print("¡AdminLTE instalado correctamente!")

if __name__ == "__main__":
    try:
        descargar_adminlte()
    except Exception as e:
        print(f"Error al instalar AdminLTE: {e}")
        print("\nDescarga manual:")
        print("1. Ve a https://adminlte.io/")
        print("2. Descarga AdminLTE")
        print("3. Copia la carpeta 'dist/' a 'app/static/adminlte/'")
