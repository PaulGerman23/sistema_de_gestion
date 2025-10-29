from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.Integer, default=1)
    productos = db.relationship('Producto', backref='categoria', lazy=True)

class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True)
    razon_social = db.Column(db.String(200), nullable=False)
    codigo_proveedor = db.Column(db.Integer, unique=True, nullable=False)
    cuit = db.Column(db.String(20), unique=True, nullable=False)
    nombre_contacto = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    email = db.Column(db.String(100))
    condicion_iva = db.Column(db.String(50))
    estado = db.Column(db.Integer, default=1)
    productos = db.relationship('Producto', backref='proveedor', lazy=True)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.Integer, unique=True, nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    precio_costo = db.Column(db.Float, nullable=False)
    precio_venta = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    estado = db.Column(db.Integer, default=1)
    detalles_venta = db.relationship('DetalleVenta', backref='producto', lazy=True)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    codigo_cliente = db.Column(db.Integer, unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    dni = db.Column(db.String(20))
    cuit = db.Column(db.String(20), unique=True)
    condicion_iva = db.Column(db.String(50))
    estado = db.Column(db.Integer, default=1)
    ventas = db.relationship('Venta', backref='cliente', lazy=True)

class RolUsuario(db.Model):
    __tablename__ = 'rol_usuarios'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), unique=True, nullable=False)
    usuarios = db.relationship('Usuario', backref='rol', lazy=True)

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol_usuarios.id'), nullable=False)
    status = db.Column(db.Integer, default=1)
    ventas = db.relationship('Venta', backref='usuario', lazy=True)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    fecha = db.Column(db.String(50), nullable=False)
    total = db.Column(db.Float, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo_pago = db.Column(db.String(50), nullable=False)
    observacion = db.Column(db.Text)
    codigo_venta = db.Column(db.Integer, unique=True, nullable=False)
    estado = db.Column(db.Integer, default=1)
    estado_venta = db.Column(db.Integer, default=1)
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True)

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_ventas'
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer, default=1)

def crear_bd():
    db.create_all()
    
    if RolUsuario.query.count() == 0:
        roles = [
            RolUsuario(tipo='superadmin'),
            RolUsuario(tipo='admin'),
            RolUsuario(tipo='ventas'),
            RolUsuario(tipo='caja'),
            RolUsuario(tipo='mecanico')
        ]
        for rol in roles:
            db.session.add(rol)
        db.session.commit()
    
    if Categoria.query.count() == 0:
        categorias = [
            Categoria(nombre='Repuestos'),
            Categoria(nombre='Herramientas'),
            Categoria(nombre='Accesorios')
        ]
        for cat in categorias:
            db.session.add(cat)
        db.session.commit()
    
    if Proveedor.query.count() == 0:
        proveedores = [
            Proveedor(razon_social='Proveedor ABC SA', codigo_proveedor=1001, cuit='20-12345678-9', 
                     nombre_contacto='Juan Pérez', telefono='1234567890', direccion='Calle 123',
                     email='contacto@abc.com', condicion_iva='Responsable Inscripto'),
            Proveedor(razon_social='Distribuidora XYZ', codigo_proveedor=1002, cuit='20-98765432-1',
                     nombre_contacto='María García', telefono='0987654321', direccion='Avenida 456',
                     email='info@xyz.com', condicion_iva='Monotributista'),
            Proveedor(razon_social='Importadora 123', codigo_proveedor=1003, cuit='20-11223344-5',
                     nombre_contacto='Carlos López', telefono='1122334455', direccion='Boulevard 789',
                     email='ventas@importadora123.com', condicion_iva='Responsable Inscripto')
        ]
        for prov in proveedores:
            db.session.add(prov)
        db.session.commit()
    
    if Producto.query.count() == 0:
        productos = [
            Producto(codigo=1001, descripcion='Filtro de aceite', precio_costo=500.00, precio_venta=750.00, stock=50, categoria_id=1, proveedor_id=1),
            Producto(codigo=1002, descripcion='Pastillas de freno', precio_costo=1200.00, precio_venta=1800.00, stock=30, categoria_id=1, proveedor_id=1),
            Producto(codigo=1003, descripcion='Juego de llaves', precio_costo=800.00, precio_venta=1200.00, stock=20, categoria_id=2, proveedor_id=2),
            Producto(codigo=1004, descripcion='Aceite motor 10W40', precio_costo=2500.00, precio_venta=3500.00, stock=40, categoria_id=1, proveedor_id=3),
            Producto(codigo=1005, descripcion='Kit de emergencia', precio_costo=600.00, precio_venta=900.00, stock=15, categoria_id=3, proveedor_id=2)
        ]
        for prod in productos:
            db.session.add(prod)
        db.session.commit()
    
    if Usuario.query.count() == 0:
        rol_admin = RolUsuario.query.filter_by(tipo='superadmin').first()
        rol_ventas = RolUsuario.query.filter_by(tipo='ventas').first()
        
        usuario_admin = Usuario(
            name='Admin',
            lastname='Sistema',
            dni='12345678',
            username='admin',
            email='admin@sistema.com',
            phone='1234567890',
            address='Oficina Central',
            rol_id=rol_admin.id
        )
        usuario_admin.set_password('admin123')
        
        usuario_vendedor = Usuario(
            name='Juan',
            lastname='Vendedor',
            dni='87654321',
            username='vendedor',
            email='vendedor@sistema.com',
            phone='0987654321',
            address='Sucursal 1',
            rol_id=rol_ventas.id
        )
        usuario_vendedor.set_password('vendedor123')
        
        db.session.add(usuario_admin)
        db.session.add(usuario_vendedor)
        db.session.commit()
    
    if Cliente.query.count() == 0:
        clientes = [
            Cliente(nombre='Carlos', apellido='Rodriguez', codigo_cliente=1, telefono='1111111111',
                   email='carlos@email.com', direccion='Calle 1', dni='11111111', 
                   condicion_iva='Consumidor Final'),
            Cliente(nombre='Ana', apellido='Martinez', codigo_cliente=2, telefono='2222222222',
                   email='ana@email.com', direccion='Calle 2', dni='22222222',
                   condicion_iva='Monotributista')
        ]
        for cliente in clientes:
            db.session.add(cliente)
        db.session.commit()