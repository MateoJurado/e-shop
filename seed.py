from app import create_app, db
from app.models import Categoria, Producto
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("🧹 Limpiando la base de datos antigua...")

    # 1. Apagar temporalmente la protección de llaves foráneas de MySQL
    db.session.execute(text('SET FOREIGN_KEY_CHECKS = 0;'))
    
    # 2. Vaciar las tablas por completo (TRUNCATE también reinicia los IDs a 1)
    # Según tu base de datos, estas son las tablas involucradas
    db.session.execute(text('TRUNCATE TABLE detalle_pedido;'))
    db.session.execute(text('TRUNCATE TABLE pedidos;'))
    db.session.execute(text('TRUNCATE TABLE productos;'))
    db.session.execute(text('TRUNCATE TABLE categorias;'))
    
    # 3. Volver a encender la protección
    db.session.execute(text('SET FOREIGN_KEY_CHECKS = 1;'))
    db.session.commit()

    print("✅ Base de datos limpia. Cargando catálogo de wheel.ec...")

    # 4. Crear las Categorías de wheel.ec
    categorias = {
        'Motor': Categoria(nombre='Motor'),
        'Frenos': Categoria(nombre='Frenos'),
        'Suspensión': Categoria(nombre='Suspensión y Dirección'),
        'Electrico': Categoria(nombre='Sistema Eléctrico')
    }

    for cat in categorias.values():
        db.session.add(cat)
    db.session.commit()

    # 5. Crear los Productos mapeando exactamente tus imágenes
    productos_data = [
        # --- MOTOR ---
        {'nombre': 'Bomba de Agua', 'descripcion': 'Bomba de agua de alto rendimiento para refrigeración óptima del motor.', 'precio': 45.50, 'stock': 15, 'imagen': 'bomba_de_agua.jpg', 'categoria': categorias['Motor']},
        {'nombre': 'Bujía de Encendido', 'descripcion': 'Bujía con punta de platino para una mejor combustión y durabilidad.', 'precio': 5.25, 'stock': 100, 'imagen': 'bujia.jpg', 'categoria': categorias['Motor']},
        {'nombre': 'Correa de Distribución', 'descripcion': 'Correa dentada de alta resistencia térmica y mecánica.', 'precio': 28.00, 'stock': 30, 'imagen': 'correa_distribucion.jpg', 'categoria': categorias['Motor']},
        {'nombre': 'Filtro de Aceite', 'descripcion': 'Filtro de aceite premium para máxima retención de impurezas.', 'precio': 8.50, 'stock': 50, 'imagen': 'filtro_aceite.jpg', 'categoria': categorias['Motor']},

        # --- FRENOS ---
        {'nombre': 'Cilindro de Rueda', 'descripcion': 'Cilindro de freno hidráulico para respuesta inmediata.', 'precio': 22.00, 'stock': 20, 'imagen': 'cilindro_de_rueda_freno.jpeg', 'categoria': categorias['Frenos']},
        {'nombre': 'Disco de Frenos', 'descripcion': 'Disco de freno ventilado para excelente disipación de calor.', 'precio': 40.00, 'stock': 24, 'imagen': 'disco_de_frenos.jpg', 'categoria': categorias['Frenos']},
        {'nombre': 'Líquido de Frenos', 'descripcion': 'Líquido de frenos DOT 4 de alta calidad.', 'precio': 12.00, 'stock': 40, 'imagen': 'liquido_de_frenos.jpg', 'categoria': categorias['Frenos']},
        {'nombre': 'Pastillas de Freno', 'descripcion': 'Juego de pastillas de cerámica sin ruido y bajo polvo.', 'precio': 35.00, 'stock': 60, 'imagen': 'pastilla_de_frenos.jpg', 'categoria': categorias['Frenos']},

        # --- SUSPENSIÓN Y DIRECCIÓN ---
        {'nombre': 'Amortiguadores', 'descripcion': 'Amortiguadores de gas para máxima estabilidad y confort en ruta.', 'precio': 85.00, 'stock': 16, 'imagen': 'amortiguadores.jpg', 'categoria': categorias['Suspensión']},
        {'nombre': 'Axiales de Dirección', 'descripcion': 'Articulación axial robusta para una dirección alineada y precisa.', 'precio': 18.50, 'stock': 25, 'imagen': 'axiales_direccion.png', 'categoria': categorias['Suspensión']},
        {'nombre': 'Rótulas de Dirección', 'descripcion': 'Rótula forjada de alta resistencia a impactos.', 'precio': 15.00, 'stock': 35, 'imagen': 'rotulas_de_direccion.jpg', 'categoria': categorias['Suspensión']},
        {'nombre': 'Terminales de Dirección', 'descripcion': 'Terminal de dirección con recubrimiento anticorrosión.', 'precio': 14.50, 'stock': 30, 'imagen': 'terminales_de_direccion.jpg', 'categoria': categorias['Suspensión']},

        # --- SISTEMA ELÉCTRICO ---
        {'nombre': 'Alternador', 'descripcion': 'Alternador de 12V y 90A para carga eficiente de batería.', 'precio': 120.00, 'stock': 8, 'imagen': 'alternador.jpg', 'categoria': categorias['Electrico']},
        {'nombre': 'Batería de Carro', 'descripcion': 'Batería de 12V libre de mantenimiento con alto poder de arranque.', 'precio': 95.00, 'stock': 12, 'imagen': 'bateria_carro.jpg', 'categoria': categorias['Electrico']},
        {'nombre': 'Bobina de Encendido', 'descripcion': 'Bobina de alto voltaje para un arranque rápido y suave.', 'precio': 42.00, 'stock': 18, 'imagen': 'bobina_de_encendido.jpg', 'categoria': categorias['Electrico']},
        {'nombre': 'Motor de Arranque', 'descripcion': 'Motor de arranque de 1.4 kW, potente y duradero.', 'precio': 110.00, 'stock': 10, 'imagen': 'motor_arranque.jpg', 'categoria': categorias['Electrico']}
    ]

    for p_data in productos_data:
        nuevo_producto = Producto(
            nombre=p_data['nombre'],
            descripcion=p_data['descripcion'],
            precio=p_data['precio'],
            stock=p_data['stock'],
            imagen=p_data['imagen'],
            categoria=p_data['categoria']
        )
        db.session.add(nuevo_producto)

    db.session.commit()
    print("¡Catálogo de wheel.ec cargado exitosamente y sin basura!")