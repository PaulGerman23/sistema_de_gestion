from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Producto, Categoria, Proveedor
from app.forms import ProductoForm
from app.routes.auth import role_required

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventario')

@inventory_bp.route('/')
@login_required
@role_required('superadmin', 'admin', 'ventas')
def listar():
    productos = Producto.query.filter_by(estado=1).all()
    return render_template('inventory/listar.html', productos=productos)

@inventory_bp.route('/agregar', methods=['GET', 'POST'])
@login_required
@role_required('superadmin', 'admin')
def agregar():
    form = ProductoForm()
    form.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.filter_by(estado=1).all()]
    form.proveedor_id.choices = [(p.id, p.razon_social) for p in Proveedor.query.filter_by(estado=1).all()]
    
    if form.validate_on_submit():
        producto_existe = Producto.query.filter_by(codigo=form.codigo.data).first()
        if producto_existe:
            flash('Ya existe un producto con ese código.', 'danger')
            return render_template('inventory/agregar_editar.html', form=form, titulo='Agregar Producto')
        
        producto = Producto(
            codigo=form.codigo.data,
            descripcion=form.descripcion.data,
            precio_costo=form.precio_costo.data,
            precio_venta=form.precio_venta.data,
            stock=form.stock.data,
            categoria_id=form.categoria_id.data,
            proveedor_id=form.proveedor_id.data
        )
        db.session.add(producto)
        db.session.commit()
        flash('Producto agregado exitosamente.', 'success')
        return redirect(url_for('inventory.listar'))
    
    return render_template('inventory/agregar_editar.html', form=form, titulo='Agregar Producto')

@inventory_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('superadmin', 'admin')
def editar(id):
    producto = Producto.query.get_or_404(id)
    form = ProductoForm(obj=producto)
    form.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.filter_by(estado=1).all()]
    form.proveedor_id.choices = [(p.id, p.razon_social) for p in Proveedor.query.filter_by(estado=1).all()]
    
    if form.validate_on_submit():
        if form.codigo.data != producto.codigo:
            producto_existe = Producto.query.filter_by(codigo=form.codigo.data).first()
            if producto_existe:
                flash('Ya existe un producto con ese código.', 'danger')
                return render_template('inventory/agregar_editar.html', form=form, producto=producto, titulo='Editar Producto')
        
        producto.codigo = form.codigo.data
        producto.descripcion = form.descripcion.data
        producto.precio_costo = form.precio_costo.data
        producto.precio_venta = form.precio_venta.data
        producto.stock = form.stock.data
        producto.categoria_id = form.categoria_id.data
        producto.proveedor_id = form.proveedor_id.data
        
        db.session.commit()
        flash('Producto actualizado exitosamente.', 'success')
        return redirect(url_for('inventory.listar'))
    
    return render_template('inventory/agregar_editar.html', form=form, producto=producto, titulo='Editar Producto')

@inventory_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@role_required('superadmin', 'admin')
def eliminar(id):
    producto = Producto.query.get_or_404(id)
    producto.estado = 0
    db.session.commit()
    flash('Producto eliminado exitosamente.', 'success')
    return redirect(url_for('inventory.listar'))