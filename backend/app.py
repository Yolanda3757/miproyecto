from flask import Flask, request, jsonify
from flask_cors import CORS
from conexion_sqlserver import obtener_tareas, crear_tarea, get_connection

app = Flask(__name__)
CORS(app)   # habilita CORS globalmente

# ✅ Listar tareas
@app.route("/tareas", methods=["GET"])
def listar_tareas():
    try:
        tareas = obtener_tareas()
        return jsonify(tareas)
    except Exception as e:
        print("❌ Error en listar_tareas:", e)
        return jsonify({"error": str(e)}), 500

# ✅ Crear tarea
@app.route("/tareas", methods=["POST"])
def nueva_tarea():
    try:
        data = request.json
        print("📩 Datos recibidos:", data)
        crear_tarea(data["titulo"], data["descripcion"])
        print("✅ Tarea insertada en BD")
        return jsonify({"mensaje": "Tarea creada correctamente"})
    except Exception as e:
        print("❌ Error en nueva_tarea:", e)
        return jsonify({"error": str(e)}), 500

# ✅ Eliminar tarea
@app.route("/tareas/<int:id>", methods=["DELETE"])
def eliminar_tarea(id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tareas WHERE id = ?", (id,))
        conn.commit()
        return jsonify({"mensaje": "Tarea eliminada"}), 200
    except Exception as e:
        print("❌ Error al eliminar tarea:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# ✅ Editar tarea
@app.route("/tareas/<int:id>", methods=["PUT"])
def editar_tarea(id):
    data = request.get_json()
    titulo = data.get("titulo")
    descripcion = data.get("descripcion")
    estado = data.get("estado")   # 👈 nuevo campo

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE tareas SET titulo = ?, descripcion = ?, estado = ? WHERE id = ?",
            (titulo, descripcion, estado, id)   # 👈 incluimos estado
        )      
        conn.commit()
        return jsonify({"mensaje": "Tarea actualizada"}), 200
    except Exception as e:
        print("❌ Error al editar tarea:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)

