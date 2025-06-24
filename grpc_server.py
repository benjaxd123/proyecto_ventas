import grpc
from concurrent import futures
import traceback

from app import create_app, db
from app.models import Sucursal
from app.proto import sucursal_pb2, sucursal_pb2_grpc

flask_app = create_app()

class SucursalService(sucursal_pb2_grpc.SucursalServiceServicer):
    def ValidarYGuardar(self, request, context):
        try:
            with flask_app.app_context():
                print(f"📦 Recibido: {request.nombre}, cantidad={request.cantidad}, precio={request.precio}, foto={request.foto}")

                if not request.nombre or request.cantidad <= 0 or request.precio <= 0:
                    return sucursal_pb2.SucursalResponse(success=False, message="Datos inválidos")

                nueva_sucursal = Sucursal(
                    nombre=request.nombre,
                    cantidad=request.cantidad,
                    precio=request.precio,
                    foto=request.foto
                )

                db.session.add(nueva_sucursal)
                db.session.commit()

                return sucursal_pb2.SucursalResponse(success=True, message="Sucursal guardada correctamente")
        except Exception as e:
            print("❌ ERROR en ValidarYGuardar:")
            traceback.print_exc()
            db.session.rollback()
            return sucursal_pb2.SucursalResponse(success=False, message=f"Error interno: {str(e)}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sucursal_pb2_grpc.add_SucursalServiceServicer_to_server(SucursalService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("🟢 Servidor gRPC corriendo en el puerto 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
