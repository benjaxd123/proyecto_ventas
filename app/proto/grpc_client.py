import grpc
from . import sucursal_pb2, sucursal_pb2_grpc

def enviar_sucursal_grpc(nombre, cantidad, precio, foto):
    try:
        channel = grpc.insecure_channel('localhost:50051')
        stub = sucursal_pb2_grpc.SucursalServiceStub(channel)

        request = sucursal_pb2.SucursalRequest(
            nombre=nombre,
            cantidad=cantidad,
            precio=precio,
            foto=foto or ""
        )

        response = stub.ValidarYGuardar(request)
        return response

    except grpc.RpcError as e:
        print(f"❌ Error al conectar con el servidor gRPC: {e}")
        # Creamos una respuesta falsa con fallo
        return sucursal_pb2.SucursalResponse(success=False, message="No se pudo contactar con el servidor gRPC")
