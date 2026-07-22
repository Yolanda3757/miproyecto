import requests
import random

API_URL = "http://127.0.0.1:5000/tareas"

# Listas de posibles títulos y descripciones
titulos = [
    "Practicar SQL",
    "Estudiar inglés",
    "Revisar correo",
    "Hacer simulacro ISTQB",
    "Ver curso de automatización"
]

descripciones = [
    "Generada automáticamente por el bot",
    "Pendiente de completar esta semana",
    "Tarea creada como recordatorio",
    "Agendada por script externo",
    "Tarea aleatoria para practicar"
]

def crear_tarea():
    tarea = {
        "titulo": random.choice(titulos),
        "descripcion": random.choice(descripciones),
        "estado": "pendiente"
    }
    try:
        res = requests.post(API_URL, json=tarea)
        if res.status_code in (200, 201):  # acepta 200 y 201 como éxito
            print("✅ Tarea creada por el bot:", res.json())
        else:
            print("⚠️ Error creando tarea:", res.text)
    except Exception as e:
        print("❌ No se pudo conectar al servidor:", e)

if __name__ == "__main__":
    crear_tarea()