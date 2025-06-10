from flask import Flask, render_template, request, redirect, url_for, flash
from app import create_app, db
from app.models import Sucursal
from werkzeug.utils import secure_filename
import os
app = create_app()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form.get('Nombre')
        cantidad = int(request.form.get('Cantidad'))
        precio = float(request.form.get('precio'))
        foto = request.files.get('foto')

        if not nombre or cantidad <= 0 or precio <= 0:
            flash('Datos inválidos')
            return redirect(url_for('agregar'))

        filename = None
        if foto:
            filename = secure_filename(foto.filename)
            ruta_fotos = os.path.join('static', 'fotos')
            os.makedirs(ruta_fotos, exist_ok=True)
            foto.save(os.path.join(ruta_fotos, filename))

        nueva_sucursal = Sucursal(
            nombre=nombre,
            cantidad=cantidad,
            precio=precio,
            foto=filename
        )
        db.session.add(nueva_sucursal)
        db.session.commit()
        flash('Sucursal agregada exitosamente.')
        return redirect(url_for('home'))

    return render_template('agregar.html')
if __name__ == '__main__':
    app.run(debug=True)

