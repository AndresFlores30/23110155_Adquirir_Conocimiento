import json
import os
from difflib import SequenceMatcher

KB_FILE = "Conocimiento.json"

# ---------------------------
# 1) Base de conocimiento inicial (precargada)
# ---------------------------
DEFAULT_KB = {
    "hola": "¡Hola! Soy Bodoque tu confiable chatbot",
    "como estas": "Bien ¿y tú?",
    "de que te gustaria hablar": "No lo se, descubramoslo"
}

# ---------------------------
# 2) Cargar / Guardar KB
# ---------------------------
def load_kb():
    if os.path.exists(KB_FILE):
        try:
            with open(KB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # Si no existe o falla, regresa la KB por defecto
    return DEFAULT_KB.copy()

def save_kb(kb):
    with open(KB_FILE, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)

# ---------------------------
# 3) Normalización simple del texto
# ---------------------------
def normalize(text: str) -> str:
    text = text.strip().lower()
    # Normalizaciones mínimas
    replacements = {
        "¿": "", "?": "",
        "¡": "", "!": "",
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "ñ": "n"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Quitar dobles espacios
    text = " ".join(text.split())
    return text

# ---------------------------
# 4) Buscar el mejor match (fuzzy básico)
# ---------------------------
def best_match(user_input, kb_keys):
    best_key = None
    best_score = 0.0

    for key in kb_keys:
        score = SequenceMatcher(None, user_input, key).ratio()
        if score > best_score:
            best_score = score
            best_key = key

    return best_key, best_score

# ---------------------------
# 5) Chat principal con adquisición de conocimiento
# ---------------------------
def run_chat():
    kb = load_kb()
    print("Chat listo. Escribe 'salir' para terminar.\n")

    THRESHOLD = 0.78  # Ajusta qué tan “estricto” quieres el match

    while True:
        user = input("Tú: ")
        if normalize(user) == "salir":
            print("Bodoque: ¡Listo! Nos vemos")
            break

        user_n = normalize(user)
        key, score = best_match(user_n, kb.keys())

        # Si el match es suficientemente bueno → responde
        if key is not None and score >= THRESHOLD:
            print(f"Bodoque: {kb[key]}")
            continue

        # Si NO hay match perfecto → módulo de adquisición
        print("Bodoque: No tengo una respuesta exacta para eso todavía.")
        teach = input("Bodoque: ¿Qué debería responder cuando me preguntan eso?: ").strip()

        if teach:
            # Guardamos exactamente la forma normalizada de la pregunta
            kb[user_n] = teach
            save_kb(kb)
            print("Bodoque: ¡Gracias! Ya lo aprendí")
        else:
            print("Bodoque: Está bien, no aprendí nada nuevo esta vez.")

# ---------------------------
# Ejecutar
# ---------------------------
if __name__ == "__main__":
    run_chat()