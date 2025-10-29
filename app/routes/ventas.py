from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Producto, Venta, DetalleVenta, Cliente
from datetime import datetime

ventas_bp = Blueprint('ventas', __name__, url_prefix='/ventas')

@ventas_bp.route('/')
@login_required
def index():
    productos = Producto.query.filter_by(estado=1).all()
    clientes = Cliente.query.filter_by(estado=1).all()
    return render_template('ventas/ventas.html', productos=productos, clientes=clientes)

@ventas_bp.route('/buscar')
@login_required
def buscar():
    termino = request.args.get('q', '')
    if termino:
        productos = Producto.query.filter(
            Producto.estado == 1,
            (Producto.descripcion.like(f'%{termino}%')) | 
            (Producto.codigo == termino if termino.isdigit() else False)
        ).limit(10).all()
        
        resultado = []
        for p in productos:
            resultado.append({
                'id': p.id,
                'codigo': p.codigo,
                'descripcion': p.descripcion,
                'precio': float(p.precio_venta),
                'stock': p.stock
            })
        return jsonify(resultado)
    
    return jsonify([])

@ventas_bp.route('/finalizar', methods=['POST'])
@login_required
def finalizar():
    try:
        datos = request.get_json()
        carrito = datos.get('carrito', [])
        cliente_id = datos.get('cliente_id')
        tipo_pago = datos.get('tipo_pago')
        observacion = datos.get('observacion', '')
        
        if not carrito:
            return jsonify({'success': False, 'message': 'El carrito está vacío.'}), 400
        
        if not tipo_pago:
            return jsonify({'success': False, 'message': 'Debe seleccionar un tipo de pago.'}), 400
        
        total = 0
        for item in carrito:
            producto = Producto.query.get(item['id'])
            if not producto or producto.estado == 0:
                return jsonify({'success': False, 'message': f'Producto {item["id"]} no encontrado.'}), 400
            
            if producto.stock < item['cantidad']:
                return jsonify({'success': False, 'message': f'Stock insuficiente para {producto.descripcion}.'}), 400
            
            total += producto.precio_venta * item['cantidad']
        
        ultima_venta = Venta.query.order_by(Venta.codigo_venta.desc()).first()
        codigo_venta = (ultima_venta.codigo_venta + 1) if ultima_venta else 1
        
        venta = Venta(
            cliente_id=cliente_id if cliente_id else None,
            fecha=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            total=total,
            usuario_id=current_user.id,
            tipo_pago=tipo_pago,
            observacion=observacion,
            codigo_venta=codigo_venta
        )
        db.session.add(venta)
        db.session.flush()
        
        for item in carrito:
            producto = Producto.query.get(item['id'])
            subtotal = producto.precio_venta * item['cantidad']
            
            detalle = DetalleVenta(
                venta_id=venta.id,
                producto_id=producto.id,
                cantidad=item['cantidad'],
                precio_unitario=producto.precio_venta,
                subtotal=subtotal
            )
            db.session.add(detalle)
            
            producto.stock -= item['cantidad']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Venta registrada exitosamente.',
            'codigo_venta': codigo_venta,
            'total': total
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error al procesar la venta: {str(e)}'}), 500