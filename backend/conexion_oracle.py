import oracledb

# Configuración de conexión en modo Thin (sin Instant Client)
username = "system"          # o el usuario que creaste
password = "Cambiar2026"        # la contraseña que definiste
dsn = "localhost:1521/xe"    # servicio de Oracle (puede ser XE o XEPDB1)

try:
    conn = oracledb.connect(user=username, password=password, dsn=dsn)
    cursor = conn.cursor()

    # Insertar una tarea de prueba
    cursor.execute("""
        INSERT INTO tareas (titulo, descripcion)
        VALUES (:titulo, :descripcion)
    """, titulo="Comprar leche", descripcion="Ir al supermercado")
    conn.commit()

    # Consultar todas las tareas
    cursor.execute("SELECT id, titulo, descripcion, estado FROM tareas")
    for row in cursor:
        print(row)

    cursor.close()
    conn.close()
    print("Conexión y operaciones realizadas con éxito.")

except Exception as e:
    print("Error al conectar o ejecutar:", e)
