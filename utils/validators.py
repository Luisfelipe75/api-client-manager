import re

def validate_password_strength(password: str) -> bool:
    """
    Reglas: 10-20 chars, al menos una mayúscula, una minúscula y un número.
    """
    if not (10 <= len(password) <= 20):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True

def validate_phone(phone: str) -> bool:
    # Ajusta el regex según el formato que requiera el API de Innovasoft
    return bool(re.match(r"^\+?1?\d{9,15}$", phone))