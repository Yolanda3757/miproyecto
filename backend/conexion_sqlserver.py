import pyodbc

def get_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-D4U4HUU;'          # 👈 instancia por defecto
        'DATABASE=TaskManager;'            # 👈 tu base de datos
        'Trusted_Connection=yes;'          # 👈 Windows Authentication
        'Encrypt=yes;'
        'TrustServerCertificate=yes;'
    )
    return conn


def obtener_tareas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, descripcion, estado, fecha_creacion FROM tareas")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

def crear_tarea(titulo, descripcion):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO tareas (titulo, descripcion, estado, fecha_creacion) VALUES (?, ?, 'pendiente', GETDATE())",
            (titulo, descripcion)
        )
        conn.commit()
        print("✅ Tarea insertada:", titulo, descripcion)
    except Exception as e:
        print("❌ Error al insertar tarea:", e)
    finally:
        conn.close()
