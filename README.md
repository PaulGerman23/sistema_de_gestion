# Sistema de Gestión con Flask + AdminLTE

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Descargar AdminLTE y copiar carpeta dist/ a app/static/adminlte/

4. Ejecutar aplicación:
```bash
python run.py
```

## Usuarios de Prueba

- **Admin**: usuario: `admin`, contraseña: `admin123`
- **Vendedor**: usuario: `vendedor`, contraseña: `vendedor123`

## Estructura del Proyecto
```
proyecto/
├── run.py
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── forms.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── inventory.py
│   │   └── ventas.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── inventory/
│   │   │   ├── listar.html
│   │   │   └── agregar_editar.html
│   │   └── ventas/
│   │       └── ventas.html
│   └── static/
│       └── adminlte/  # Copiar aquí el contenido de dist/ de AdminLTE
```

## Características

- Autenticación con Flask-Login
- Control de roles (superadmin, admin, ventas, caja, mecanico)
- Gestión de inventario (CRUD productos)
- Sistema de ventas con carrito
- Dashboard con estadísticas y gráficos
- Diseño responsivo con AdminLTE
- Notificaciones con SweetAlert2