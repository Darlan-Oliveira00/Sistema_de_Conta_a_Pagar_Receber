from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from base64 import b64encode, b64decode
from dotenv import load_dotenv
import hashlib
import secrets
import bcrypt
import hmac
import os

load_dotenv()

HASH_SALT = os.getenv("HASH_SALT").encode()
CRYPTO_TOKEN = bytes.fromhex(os.getenv("CRYPTO_TOKEN"))

def HASH_cpf(cpf:str) -> str:
    return hmac.new(HASH_SALT, cpf.encode(), hashlib.sha256).hexdigest()

def criptografar_cpf(cpf: str) -> str:
    aesgcm = AESGCM(CRYPTO_TOKEN)
    iv = secrets.token_bytes(12)
    cifrado = aesgcm.encrypt(iv, cpf.encode(), None)
    return b64encode(iv).decode() + ':' + b64encode(cifrado).decode()


def descriptografar_cpf(dado: str) -> str:
    iv_b64, cifrado_b64 = dado.split(':')
    iv = b64decode(iv_b64)
    cifrado = b64decode(cifrado_b64)
    aesgcm = AESGCM(CRYPTO_TOKEN)
    return aesgcm.decrypt(iv, cifrado, None).decode()

def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt(rounds=10)).decode()

def verificar_senha(senha: str, hash_salvo: str) -> bool:
    return bcrypt.checkpw(senha.encode(), hash_salvo.encode())
