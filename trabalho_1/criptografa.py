import bcrypt

def criptografar_senha(senha) -> str:

    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'),salt)
    return senha_hash.decode('utf-8')
    
def verificar_senha(senha_digitada,senha_hash) -> bool:

    return bcrypt.checkpw(
        senha_digitada.encode('utf-8'),
        senha_hash.encode('utf-8')
        )
