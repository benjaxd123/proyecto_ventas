from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from app import create_app
from app.proto.grpc_client import enviar_sucursal_grpc
from flask import Response
import time
from app.models import Sucursal
eventos_sse = []

app = create_app()

@app.route('/')
def home():
    sucursales = Sucursal.query.all()
    return render_template('index.html', sucursales=sucursales)


@app.route('/sse')
def stream_sse():
    def event_stream():
        prev_len = 0
        while True:
            if len(eventos_sse) > prev_len:
                mensaje = eventos_sse[-1]
                yield f"data: {mensaje}\n\n"
                prev_len = len(eventos_sse)
            time.sleep(1)
    return Response(event_stream(), mimetype='text/event-stream')

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form.get('Nombre')
        cantidad_str = request.form.get('Cantidad')
        precio_str = request.form.get('precio')

        # Valida que los campos no esten vacíos
        if not nombre or not cantidad_str or not precio_str:
            flash("❌ Debes ingresar todos los datos.")
            eventos_sse.append("❌ Faltan campos obligatorios")
            return redirect(url_for('agregar'))

        # Convertir si ya pasó la validación
        cantidad = int(cantidad_str)
        precio = float(precio_str)
        foto = request.files.get('foto')
        filename = None
        if foto:
            filename = secure_filename(foto.filename)
            ruta_fotos = os.path.join(app.root_path, 'static', 'fotos')
            os.makedirs(ruta_fotos, exist_ok=True)
            foto.save(os.path.join(ruta_fotos, filename))
        
        # Llamada al cliente gRPC
        respuesta = enviar_sucursal_grpc(nombre, cantidad, precio, filename or "")

        if not respuesta.success:
            flash(f"❌ Error: {respuesta.message}")
            eventos_sse.append(f"❌ Error al agregar '{nombre}': {respuesta.message}")

            return redirect(url_for('agregar'))

        flash("✅ Sucursal agregada exitosamente (vía gRPC).")
        eventos_sse.append(f"✅ Sucursal '{nombre}' agregada correctamente")

        return redirect(url_for('home'))

    return render_template('agregar.html')

if __name__ == '__main__':
    app.run(debug=True)
