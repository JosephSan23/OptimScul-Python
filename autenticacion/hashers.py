import bcrypt

def verificar_password(password_plano, hash_guardado):
    try:
        password_bytes = password_plano.encode('utf-8')
        hash_bytes = hash_guardado.encode('utf-8')
        
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except (ValueError, TypeError):
        return False