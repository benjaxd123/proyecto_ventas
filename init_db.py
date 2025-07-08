from app import create_app, db
from app.models import Sucursal

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    sucursales = [
        #Sucursal(nombre="Sucursal 1", cantidad=31, precio=333),
        #Sucursal(nombre="Casa Matriz", cantidad=10, precio=999),
        Sucursal(nombre="Vasos", cantidad=30, precio=2500, foto="vasos.jpg"),
        Sucursal(nombre="Platos", cantidad=30, precio=2500, foto="platos.jpg"),
    ]

    db.session.bulk_save_objects(sucursales)
    db.session.commit()
    print("✅ Base de datos inicializada.")
