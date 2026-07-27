<<<<<<< HEAD
from flask import render_template
from . import admin_bp
from flask_login import login_required
from .decorators import admin_requerido

=======
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models import Categoria, Producto, Usuario, Pedido
from . import admin_bp
from .decorators import admin_requerido


# ==================================================
# DASHBOARD
# ==================================================

>>>>>>> f7d16a8be16f03e7db395170a45e982b073714e8
@admin_bp.route('/dashboard')
@login_required
@admin_requerido
def dashboard():
<<<<<<< HEAD
    return render_template('admin/home.html')

@admin_bp.route('/admin/productos')
def productos():
    return render_template('admin/productos.html')

@admin_bp.route('/admin/clientes')
def clientes():
    return render_template('admin/clientes.html')

@admin_bp.route('/admin/pedidos')
def pedidos():
    return render_template('admin/pedidos.html')

=======

    total_productos = Producto.query.filter_by(activo=True).count()

    total_clientes = Usuario.query.filter_by(
        rol='cliente',
        activo=True
    ).count()

    total_pedidos = Pedido.query.count()

    ventas_totales = db.session.query(
        db.func.sum(Pedido.total)
    ).scalar() or 0

    bajo_stock = Producto.query.filter(
        Producto.stock <= 5,
        Producto.activo == True
    ).count()

    return render_template(

        "admin/home.html",

        total_productos=total_productos,
        total_clientes=total_clientes,
        total_pedidos=total_pedidos,
        ventas_totales=ventas_totales,
        bajo_stock=bajo_stock

    )


# ==================================================
# CATEGORÍAS
# ==================================================

@admin_bp.route('/categorias')
@login_required
@admin_requerido
def categorias():

    categorias = Categoria.query.filter_by(activa=True)\
                                .order_by(Categoria.id.desc())\
                                .all()

    return render_template(
        'admin/categorias.html',
        categorias=categorias
    )


@admin_bp.route('/categorias/nueva', methods=['GET', 'POST'])
@login_required
@admin_requerido
def nueva_categoria():

    if request.method == 'POST':

        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()

        if not nombre:
            flash('El nombre es obligatorio.', 'danger')
            return redirect(url_for('admin.nueva_categoria'))

        existe = Categoria.query.filter_by(nombre=nombre).first()

        if existe:
            flash('Ya existe una categoría con ese nombre.', 'warning')
            return redirect(url_for('admin.nueva_categoria'))

        categoria = Categoria(
            nombre=nombre,
            descripcion=descripcion
        )

        db.session.add(categoria)
        db.session.commit()

        flash('Categoría creada correctamente.', 'success')

        return redirect(url_for('admin.categorias'))

    return render_template('admin/categoria_form.html')


@admin_bp.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_requerido
def editar_categoria(id):

    categoria = Categoria.query.get_or_404(id)

    if request.method == 'POST':

        categoria.nombre = request.form.get('nombre').strip()
        categoria.descripcion = request.form.get('descripcion').strip()

        db.session.commit()

        flash('Categoría actualizada.', 'success')

        return redirect(url_for('admin.categorias'))

    return render_template(
        'admin/categoria_form.html',
        categoria=categoria
    )


@admin_bp.route('/categorias/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_requerido
def eliminar_categoria(id):

    categoria = Categoria.query.get_or_404(id)

    categoria.activa = False

    db.session.commit()

    flash('Categoría eliminada.', 'success')

    return redirect(url_for('admin.categorias'))


# ==================================================
# PRODUCTOS
# ==================================================

@admin_bp.route('/productos')
@login_required
@admin_requerido
def productos():

    productos = Producto.query.filter_by(activo=True)\
                              .order_by(Producto.id.desc())\
                              .all()

    return render_template(
        'admin/productos.html',
        productos=productos
    )


@admin_bp.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
@admin_requerido
def nuevo_producto():

    categorias = Categoria.query.filter_by(activa=True).all()

    if request.method == 'POST':

        producto = Producto(
            nombre=request.form.get('nombre'),
            descripcion=request.form.get('descripcion'),
            precio=request.form.get('precio'),
            stock=request.form.get('stock'),
            categoria_id=request.form.get('categoria_id'),
            imagen=None
        )

        db.session.add(producto)
        db.session.commit()

        flash('Producto creado correctamente.', 'success')

        return redirect(url_for('admin.productos'))

    return render_template(
        'admin/producto_form.html',
        categorias=categorias,
        producto=None
    )

@admin_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_requerido
def editar_producto(id):

    producto = Producto.query.get_or_404(id)
    categorias = Categoria.query.filter_by(activa=True).all()

    if request.method == 'POST':

        producto.nombre = request.form.get('nombre')
        producto.descripcion = request.form.get('descripcion')
        producto.precio = request.form.get('precio')
        producto.stock = request.form.get('stock')
        producto.categoria_id = request.form.get('categoria_id')

        db.session.commit()

        flash('Producto actualizado correctamente.', 'success')

        return redirect(url_for('admin.productos'))

    return render_template(
        'admin/producto_form.html',
        producto=producto,
        categorias=categorias
    )

@admin_bp.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_requerido
def eliminar_producto(id):

    producto = Producto.query.get_or_404(id)

    producto.activo = False

    db.session.commit()

    flash('Producto eliminado correctamente.', 'success')

    return redirect(url_for('admin.productos'))
# ==================================================
# CLIENTES
# ==================================================

@admin_bp.route('/clientes')
@login_required
@admin_requerido
def clientes():

    clientes = Usuario.query.filter_by(
        rol='cliente'
    ).order_by(
        Usuario.id.desc()
    ).all()

    return render_template(
        'admin/clientes.html',
        clientes=clientes
    )

@admin_bp.route('/clientes/toggle/<int:id>', methods=['POST'])
@login_required
@admin_requerido
def toggle_cliente(id):

    cliente = Usuario.query.get_or_404(id)

    cliente.activo = not cliente.activo

    db.session.commit()

    flash(
        'Estado del cliente actualizado.',
        'success'
    )

    return redirect(
        url_for('admin.clientes')
    )

# ==================================================
# PEDIDOS
# ==================================================

@admin_bp.route('/pedidos')
@login_required
@admin_requerido
def pedidos():

    pedidos = Pedido.query.order_by(
        Pedido.fecha.desc()
    ).all()

    return render_template(
        'admin/pedidos.html',
        pedidos=pedidos
    )

@admin_bp.route('/pedidos/<int:id>/estado', methods=['POST'])
@login_required
@admin_requerido
def cambiar_estado(id):

    pedido = Pedido.query.get_or_404(id)

    siguiente_estado = {
        "pendiente": "pagado",
        "pagado": "enviado",
        "enviado": "entregado"
    }

    if pedido.estado in siguiente_estado:
        pedido.estado = siguiente_estado[pedido.estado]
        db.session.commit()
        flash("Estado actualizado.", "success")
    else:
        flash("El pedido ya no puede cambiar de estado.", "warning")

    return redirect(url_for("admin.pedidos"))
>>>>>>> f7d16a8be16f03e7db395170a45e982b073714e8
