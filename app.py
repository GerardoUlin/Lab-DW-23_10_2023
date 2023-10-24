from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos MySQL
conexion = mysql.connector.connect(
    host="127.0.0.1",  # Cambia a tu host
    user="root",  # Cambia a tu usuario
    password="Ulin",  # Cambia a tu contraseña
    database="as"  # Cambia al nombre de tu base de datos
)
cursor = conexion.cursor()

# Ruta para mostrar la lista de compras
@app.route('/')
def lista_compras():
    cursor.execute("SELECT * FROM lista_compras")
    compras = cursor.fetchall()
    return render_template('lista_compras.html', compras=compras)

# Ruta para agregar una compra
@app.route('/agregar', methods=['POST'])
def agregar_compra():
    id = request.form['id']
    nombre = request.form['nombre']
    cantidad = request.form['cantidad']
    realizado = 1 if 'realizado' in request.form else 0
    
    cursor.execute("UPDATE lista_compras SET Nombre = %s, Cantidad = %s, Realizado = %s WHERE Id = %s", (nombre, cantidad, realizado, id))
    conexion.commit()
    
    return redirect(url_for('lista_compras'))

# Ruta para actualizar una compra
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_compra(id):
    nombre = request.form['nombre']
    cantidad = request.form['cantidad']
    realizado = request.form.get('realizado', False)
    
    cursor.execute("UPDATE lista_compras SET Nombre = %s, Cantidad = %s, Realizado = %s WHERE Id = %s", (nombre, cantidad, realizado, id))
    conexion.commit()
    
    return redirect(url_for('lista_compras'))

# Ruta para borrar una compra
@app.route('/borrar/<int:id>')
def borrar_compra(id):
    cursor.execute("DELETE FROM lista_compras WHERE Id = %s", (id,))
    conexion.commit()
    
    return redirect(url_for('lista_compras'))

if __name__ == '__main__':
    app.run(debug=True)
