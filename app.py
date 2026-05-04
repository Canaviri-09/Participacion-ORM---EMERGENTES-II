from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#instanciamos la base de datos
db = SQLAlchemy(app)

class Producto(db.Model):
    __table__name__ = 'products'

    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

    def __repr__(self):
        return (f"<Producto(id={self.id}, name='{self.name}', "f"precio={self.precio}, stock={self.stock})>")


#  1. CREATE – Inicializar BD e insertar datos
def init_db():
    with app.app_context():
        db.create_all()
        print("Base de datos 'products.db' creada correctamente")

def insert_products():
    with app.app_context():
        print("\n Insertando productos")
        p1 = Producto(name="Laptop Dell",   precio=1200, stock=10)
        p2 = Producto(name="Mouse", precio=80,   stock=25)
        p3 = Producto(name="Teclado Genius",  precio=150,  stock=15)
        p4 = Producto(name="Monitor LG",   precio=600,  stock=8)
        p5 = Producto (name="Audífonos Sony",     precio=100,  stock=10)

        db.session.add_all([p1, p2, p3, p4, p5])
        db.session.commit()
        print("productos insertados correctamente")


#  2. READ – Consultas
def query_products():
    with app.app_context():
        print("\n Listado completo de productos:")
        all_products = Producto.query.all()
        for p in all_products:
            print(f"  {p}")

        print("\n Productos con precio >= 200:")
        caros = Producto.query.filter(Producto.precio >= 200).all()
        for p in caros:
            print(f"  {p}")

        print("\n Buscar producto por id=1:")
        product = Producto.query.filter_by(id=1).first()
        if product:
            print(f"  {product}")
        else:
            print("Producto no encontrado")


#  3. UPDATE – Actualizar un registro
def update_product():
    with app.app_context():
        print("\n Actualizando producto con id=2")
        product = Producto  .query.filter_by(id=2).first()
        if product:
            print(f"  Antes : {product}")
            product.name  = "Mouse Logitech MX Master 3"
            product.precio = 89.99
            product.stock = 30
            db.session.commit()
            # Re-query para mostrar el valor actualizado
            product = Producto.query.filter_by(id=2).first()
            print(f"  Después: {product}")
            print("Producto actualizado")
        else:
            print("Producto no encontrado")


#  4. DELETE – Eliminar un registro
def delete_product():
    with app.app_context():
        print("\n Eliminando producto con id=5")
        product = Producto.query.filter_by(id=5).first()
        if product:
            print(f"  Eliminando: {product}")
            db.session.delete(product)
            db.session.commit()
            print("Producto eliminado satisfactoriamente")

            # Verificamos que ya no existe
            verificacion = Producto.query.filter_by(id=5).first()
            if not verificacion:
                print("Verificación: el producto ya NO existe en la BD")
        else:
            print("Producto no encontrado")

def query_final():
    with app.app_context():
        print("\nEstado de la base de datos:")
        all_products = Producto.query.all()
        for p in all_products:
            print(f"  {p}")
        print(f"\n Total de productos en BD: {len(all_products)}")
       

if __name__ == '__main__':
    init_db()
    insert_products()
    query_products()
    update_product()
    delete_product()
    query_final()
