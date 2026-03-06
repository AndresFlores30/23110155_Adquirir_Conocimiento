import json
import os
from difflib import SequenceMatcher

KB_FILE = "Conocimiento.json"
USERS_FILE = "usuarios.json"
CITAS_FILE = "citas.json"
PEDIDOS_FILE = "pedidos.json"

# -------------------------------------------------
# 1) Base de conocimiento inicial
# -------------------------------------------------
DEFAULT_KB = {
    "hola": "¡Hola! Soy Bodoque, tu chatbot de la óptica. Puedo ayudarte a agendar citas, registrar pedidos de lentes y responder dudas.",
    "como estas": "Muy bien, gracias por preguntar. Estoy listo para ayudarte.",
    "de que te gustaria hablar": "Podemos hablar sobre citas, pedidos de lentes, examen de la vista, armazones o servicios de la óptica.",
    "que servicios ofrecen": "Ofrecemos examen de la vista, venta de armazones, lentes graduados y seguimiento de pedidos.",
    "horario": "Nuestro horario es de lunes a sábado de 10:00 am a 7:00 pm.",
    "ubicacion": "Estamos en la sucursal principal de la óptica.",
    "quiero agendar una cita": "Claro, te ayudaré a agendar una cita, empieza por escirbir: agendar cita.",
    "quiero pedir lentes": "Perfecto, te ayudaré a registrar tu pedido de lentes."
}

# Un solo usuario: admin
DEFAULT_USERS = {
    "admin": "1234"
}

# -------------------------------------------------
# 2) Funciones para archivos JSON
# -------------------------------------------------
def load_json(file_name, default_data):
    if os.path.exists(file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default_data

def save_json(file_name, data):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def initialize_files():
    if not os.path.exists(KB_FILE):
        save_json(KB_FILE, DEFAULT_KB)

    if not os.path.exists(USERS_FILE):
        save_json(USERS_FILE, DEFAULT_USERS)

    if not os.path.exists(CITAS_FILE):
        save_json(CITAS_FILE, [])

    if not os.path.exists(PEDIDOS_FILE):
        save_json(PEDIDOS_FILE, [])

# -------------------------------------------------
# 3) Base de conocimiento
# -------------------------------------------------
def load_kb():
    return load_json(KB_FILE, DEFAULT_KB.copy())

def save_kb(kb):
    save_json(KB_FILE, kb)

# -------------------------------------------------
# 4) Normalización
# -------------------------------------------------
def normalize(text: str) -> str:
    text = text.strip().lower()
    replacements = {
        "¿": "", "?": "",
        "¡": "", "!": "",
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "ñ": "n"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    text = " ".join(text.split())
    return text

# -------------------------------------------------
# 5) Buscar mejor coincidencia
# -------------------------------------------------
def best_match(user_input, kb_keys):
    best_key = None
    best_score = 0.0

    for key in kb_keys:
        score = SequenceMatcher(None, user_input, key).ratio()
        if score > best_score:
            best_score = score
            best_key = key

    return best_key, best_score

# -------------------------------------------------
# 6) Login admin
# -------------------------------------------------
def login_admin():
    users = load_json(USERS_FILE, DEFAULT_USERS.copy())

    print("Bodoque: Esta acción requiere acceso de administrador.")
    username = input("Usuario: ").strip()
    password = input("Contraseña: ").strip()

    if username in users and users[username] == password:
        print("Bodoque: Acceso de administrador concedido.")
        return True
    else:
        print("Bodoque: Usuario o contraseña incorrectos.")
        return False

# -------------------------------------------------
# 7) Agendar cita
# -------------------------------------------------
def agendar_cita():
    citas = load_json(CITAS_FILE, [])

    print("Bodoque: Vamos a registrar tu cita.")
    nombre = input("Nombre del cliente: ").strip()
    telefono = input("Teléfono: ").strip()
    fecha = input("Fecha de la cita (dd/mm/aaaa): ").strip()
    hora = input("Hora de la cita: ").strip()
    motivo = input("Motivo de la cita: ").strip()

    cita = {
        "nombre": nombre,
        "telefono": telefono,
        "fecha": fecha,
        "hora": hora,
        "motivo": motivo
    }

    citas.append(cita)
    save_json(CITAS_FILE, citas)

    print("Bodoque: Tu cita ha sido registrada correctamente.")

# -------------------------------------------------
# 8) Registrar pedido
# -------------------------------------------------
def registrar_pedido():
    pedidos = load_json(PEDIDOS_FILE, [])

    print("Bodoque: Vamos a registrar tu pedido de lentes.")
    nombre = input("Nombre del cliente: ").strip()
    telefono = input("Teléfono: ").strip()
    tipo_lente = input("Tipo de lente: ").strip()
    armazon = input("Modelo o tipo de armazón: ").strip()
    graduacion = input("Graduación o descripción: ").strip()
    fecha_entrega = input("Fecha estimada de entrega (dd/mm/aaaa): ").strip()

    pedido = {
        "nombre": nombre,
        "telefono": telefono,
        "tipo_lente": tipo_lente,
        "armazon": armazon,
        "graduacion": graduacion,
        "fecha_entrega": fecha_entrega
    }

    pedidos.append(pedido)
    save_json(PEDIDOS_FILE, pedidos)

    print("Bodoque: El pedido de lentes ha sido registrado correctamente.")

# -------------------------------------------------
# 9) Ver citas
# -------------------------------------------------
def ver_citas():
    if not login_admin():
        return

    citas = load_json(CITAS_FILE, [])

    if not citas:
        print("Bodoque: No hay citas registradas.")
        return

    print("Bodoque: Estas son las citas registradas:")
    for i, cita in enumerate(citas, start=1):
        print(f"\nCita {i}:")
        print(f"Nombre: {cita['nombre']}")
        print(f"Teléfono: {cita['telefono']}")
        print(f"Fecha: {cita['fecha']}")
        print(f"Hora: {cita['hora']}")
        print(f"Motivo: {cita['motivo']}")

# -------------------------------------------------
# 10) Ver pedidos
# -------------------------------------------------
def ver_pedidos():
    if not login_admin():
        return

    pedidos = load_json(PEDIDOS_FILE, [])

    if not pedidos:
        print("Bodoque: No hay pedidos registrados.")
        return

    print("Bodoque: Estos son los pedidos registrados:")
    for i, pedido in enumerate(pedidos, start=1):
        print(f"\nPedido {i}:")
        print(f"Nombre: {pedido['nombre']}")
        print(f"Teléfono: {pedido['telefono']}")
        print(f"Tipo de lente: {pedido['tipo_lente']}")
        print(f"Armazón: {pedido['armazon']}")
        print(f"Graduación: {pedido['graduacion']}")
        print(f"Fecha estimada de entrega: {pedido['fecha_entrega']}")

# -------------------------------------------------
# 11) Borrar cita
# -------------------------------------------------
def borrar_cita():
    if not login_admin():
        return

    citas = load_json(CITAS_FILE, [])

    if not citas:
        print("Bodoque: No hay citas registradas para borrar.")
        return

    print("Bodoque: Estas son las citas disponibles para borrar:")
    for i, cita in enumerate(citas, start=1):
        print(f"\nCita {i}:")
        print(f"Nombre: {cita['nombre']}")
        print(f"Teléfono: {cita['telefono']}")
        print(f"Fecha: {cita['fecha']}")
        print(f"Hora: {cita['hora']}")
        print(f"Motivo: {cita['motivo']}")

    try:
        indice = int(input("\nEscribe el número de la cita que deseas borrar: "))
        if 1 <= indice <= len(citas):
            cita_eliminada = citas.pop(indice - 1)
            save_json(CITAS_FILE, citas)
            print(f"Bodoque: La cita de {cita_eliminada['nombre']} fue eliminada correctamente.")
        else:
            print("Bodoque: Número inválido.")
    except ValueError:
        print("Bodoque: Debes escribir un número válido.")

# -------------------------------------------------
# 12) Borrar pedido
# -------------------------------------------------
def borrar_pedido():
    if not login_admin():
        return

    pedidos = load_json(PEDIDOS_FILE, [])

    if not pedidos:
        print("Bodoque: No hay pedidos registrados para borrar.")
        return

    print("Bodoque: Estos son los pedidos disponibles para borrar:")
    for i, pedido in enumerate(pedidos, start=1):
        print(f"\nPedido {i}:")
        print(f"Nombre: {pedido['nombre']}")
        print(f"Teléfono: {pedido['telefono']}")
        print(f"Tipo de lente: {pedido['tipo_lente']}")
        print(f"Armazón: {pedido['armazon']}")
        print(f"Graduación: {pedido['graduacion']}")
        print(f"Fecha estimada de entrega: {pedido['fecha_entrega']}")

    try:
        indice = int(input("\nEscribe el número del pedido que deseas borrar: "))
        if 1 <= indice <= len(pedidos):
            pedido_eliminado = pedidos.pop(indice - 1)
            save_json(PEDIDOS_FILE, pedidos)
            print(f"Bodoque: El pedido de {pedido_eliminado['nombre']} fue eliminado correctamente.")
        else:
            print("Bodoque: Número inválido.")
    except ValueError:
        print("Bodoque: Debes escribir un número válido.")

# -------------------------------------------------
# 13) Detectar intención
# -------------------------------------------------
def detectar_intencion(texto):
    texto = normalize(texto)

    if any(frase in texto for frase in [
        "agendar cita", "quiero una cita", "registrar cita", "hacer una cita", "sacar una cita"
    ]):
        return "agendar_cita"

    if any(frase in texto for frase in [
        "pedir lentes", "registrar pedido", "quiero lentes", "hacer pedido", "comprar lentes"
    ]):
        return "registrar_pedido"

    if any(frase in texto for frase in [
        "ver citas", "mostrar citas", "consultar citas", "lista de citas"
    ]):
        return "ver_citas"

    if any(frase in texto for frase in [
        "ver pedidos", "mostrar pedidos", "consultar pedidos", "lista de pedidos"
    ]):
        return "ver_pedidos"

    if any(frase in texto for frase in [
        "borrar cita", "eliminar cita", "quitar cita"
    ]):
        return "borrar_cita"

    if any(frase in texto for frase in [
        "borrar pedido", "eliminar pedido", "quitar pedido"
    ]):
        return "borrar_pedido"

    return None

# -------------------------------------------------
# 14) Chat principal
# -------------------------------------------------
def run_chat():
    initialize_files()
    kb = load_kb()
    THRESHOLD = 0.78

    print("Bodoque: ¡Hola! Soy tu asistente de la óptica.")
    print("Bodoque: Escribe 'salir' para terminar.\n")

    while True:
        user = input("Tú: ")

        if normalize(user) == "salir":
            print("Bodoque: Gracias por usar el sistema. Hasta luego.")
            break

        intencion = detectar_intencion(user)

        if intencion == "agendar_cita":
            agendar_cita()
            print()
            continue

        elif intencion == "registrar_pedido":
            registrar_pedido()
            print()
            continue

        elif intencion == "ver_citas":
            ver_citas()
            print()
            continue

        elif intencion == "ver_pedidos":
            ver_pedidos()
            print()
            continue

        elif intencion == "borrar_cita":
            borrar_cita()
            print()
            continue

        elif intencion == "borrar_pedido":
            borrar_pedido()
            print()
            continue

        user_n = normalize(user)
        key, score = best_match(user_n, kb.keys())

        if key is not None and score >= THRESHOLD:
            print(f"Bodoque: {kb[key]}")
            continue

        print("Bodoque: No tengo una respuesta exacta para eso todavía.")
        teach = input("Bodoque: ¿Qué debería responder cuando me pregunten eso?: ").strip()

        if teach:
            kb[user_n] = teach
            save_kb(kb)
            print("Bodoque: ¡Gracias! Ya lo aprendí.\n")
        else:
            print("Bodoque: Está bien, no aprendí nada nuevo esta vez.\n")

# -------------------------------------------------
# 15) Ejecutar
# -------------------------------------------------
if __name__ == "__main__":
    run_chat()