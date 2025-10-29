from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Producto, Venta, Cliente, Proveedor
from sqlalchemy import func
from datetime import datetime, timedelta
from app import db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    total_productos = Producto.query.filter_by(estado=1).count()
    total_ventas = Venta.query.filter_by(estado=1).count()
    total_clientes = Cliente.query.filter_by(estado=1).count()
    total_proveedores = Proveedor.query.filter_by(estado=1).count()
    
    fecha_actual = datetime.now()
    ventas_ultimos_7_dias = []
    labels_dias = []
    
    for i in range(6, -1, -1):
        fecha = fecha_actual - timedelta(days=i)
        fecha_str = fecha.strftime('%Y-%m-%d')
        labels_dias.append(fecha.strftime('%d/%m'))
        
        total_dia = db.session.query(func.sum(Venta.total)).filter(
            Venta.fecha.like(f'{fecha_str}%'),
            Venta.estado == 1
        ).scalar() or 0
        
        ventas_ultimos_7_dias.append(float(total_dia))
    
    return render_template('dashboard.html',
                         total_productos=total_productos,
                         total_ventas=total_ventas,
                         total_clientes=total_clientes,
                         total_proveedores=total_proveedores,
                         ventas_datos=ventas_ultimos_7_dias,
                         ventas_labels=labels_dias)