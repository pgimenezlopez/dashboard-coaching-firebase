import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Inicializar Firebase (asegurate de tener firebase_key.json en la misma carpeta)
def init_firebase():
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)

# Guardar una sesión de coaching
def guardar_sesion(usuario_email, cliente, fecha, claridad, objetivo, accion, estado):
    init_firebase()
    db = firestore.client()
    doc_ref = db.collection("usuarios").document(usuario_email).collection("clientes").document(cliente).collection("sesiones").document(fecha.strftime("%Y-%m-%d"))
    doc_ref.set({
        "fecha": fecha,
        "nivel_claridad": claridad,
        "objetivo": objetivo,
        "accion": accion,
        "estado": estado,
        "timestamp": datetime.utcnow()
    })

# Leer todas las sesiones de un cliente
def leer_sesiones(usuario_email, cliente):
    init_firebase()
    db = firestore.client()
    sesiones_ref = db.collection("usuarios").document(usuario_email).collection("clientes").document(cliente).collection("sesiones")
    docs = sesiones_ref.order_by("fecha").stream()
    sesiones = []
    for doc in docs:
        data = doc.to_dict()
        sesiones.append({
            "Fecha": data["fecha"].strftime("%Y-%m-%d") if isinstance(data["fecha"], datetime) else data["fecha"],
            "Nivel de claridad (1-10)": data["nivel_claridad"],
            "Objetivo de sesión": data["objetivo"],
            "Acción comprometida": data["accion"],
            "Estado de avance": data["estado"]
        })
    return sesiones
