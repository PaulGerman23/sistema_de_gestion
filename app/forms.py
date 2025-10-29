from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=4)])

class ProductoForm(FlaskForm):
    codigo = IntegerField('Código', validators=[DataRequired()])
    descripcion = StringField('Descripción', validators=[DataRequired(), Length(max=200)])
    precio_costo = FloatField('Precio Costo', validators=[DataRequired(), NumberRange(min=0)])
    precio_venta = FloatField('Precio Venta', validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    categoria_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    proveedor_id = SelectField('Proveedor', coerce=int, validators=[DataRequired()])

class VentaForm(FlaskForm):
    cliente_id = SelectField('Cliente', coerce=int, validators=[Optional()])
    tipo_pago = SelectField('Tipo de Pago', choices=[
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia')
    ], validators=[DataRequired()])
    observacion = TextAreaField('Observación', validators=[Optional()])