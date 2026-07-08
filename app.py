import hashlib
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_NAME = "usuarios.db"


# --- PASO 2.1: Gestión de la Base de Datos ---
def init_db():
    """Crea la tabla de usuarios si no existe e inserta los integrantes solicitados."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """
    )

    # Nombres de los integrantes del examen solicitados
    integrantes = ["Tomas Ponce", "Sebastian Camus", "Felipe Olave"]
    password_por_defecto = (
        "examen2026"  # Contraseña elegida para la demostración
    )

    # Generar el hash SHA-256 de la contraseña
    hashed_pw = hashlib.sha256(password_por_defecto.encode()).hexdigest()

    # Insertar cada integrante de forma segura (ignorando si ya existen)
    for nombre in integrantes:
        try:
            cursor.execute(
                "INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)",
                (nombre, hashed_pw),
            )
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()


# --- PASO 2.2: Ruta para validar usuarios ---
@app.route("/login", methods=["POST"])
def login():
    """Valida si el nombre del integrante y su contraseña coinciden con la BD."""
    data = request.get_json()

    if not data or "nombre" not in data or "password" not in data:
        return (
            jsonify({"status": "error", "message": "Faltan datos en la solicitud"}),
            400,
        )

    nombre = data["nombre"]
    password = data["password"]

    # Aplicar hash a la contraseña ingresada en el comando para poder compararla
    hashed_input = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM usuarios WHERE nombre = ? AND password_hash = ?",
        (nombre, hashed_input),
    )
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"Validación exitosa. Bienvenido/a {nombre}.",
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "status": "fail",
                    "message": "Usuario o contraseña incorrectos.",
                }
            ),
            401,
        )


# --- PASO 2.3: Servidor en puerto 7500 ---
if __name__ == "__main__":
    init_db()  # Crea la BD e integra a Tomas, Sebastian y Felipe
    print("Base de datos lista con los integrantes del examen.")
    app.run(port=7500, debug=True)
