from flask import Flask, request, jsonify
import oracledb

app = Flask(__name__)

# Configuración de conexión
username = "system"
password = "Cambiar2026"
dsn = "localhost:1521/xe"

def get_connection():
    return oracledb.connect(user=username, password=password, dsn=dsn)

# Endpoint: listar tareas
@app.route("/tasks", methods=["GET"])
def listar_tareas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, descripcion, estado FROM tareas")
    tareas = [
        {"id": row[0], "titulo": row[1], "descripcion": row[2], "estado": row[3]}
        for row in cursor
    ]
    cursor.close()
    conn.close()
    return jsonify(tareas)

# Endpoint: crear tarea
@app.route("/tasks", methods=["POST"])
def crear_tarea():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tareas (titulo, descripcion, estado)
        VALUES (:titulo, :descripcion, 'pendiente')
    """, titulo=data["titulo"], descripcion=data["descripcion"])
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Tarea creada con éxito"}), 201

if __name__ == "__main__":
    app.run(debug=True)
