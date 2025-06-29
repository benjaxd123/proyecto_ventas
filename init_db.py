from app import create_app, db
from app.models import Sucursal

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    sucursales = [
        Sucursal(nombre="Sucursal 1", cantidad=31, precio=333),
        Sucursal(nombre="Casa Matriz", cantidad=10, precio=999),
    ]

    db.session.bulk_save_objects(sucursales)
    db.session.commit()
    print("✅ Base de datos inicializada.")
