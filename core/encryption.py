import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 16  # AES block size

def derive_key(password: str) -> bytes:
    return SHA256.new(password.encode()).digest()

def encrypt_data(data: bytes, password: str) -> bytes:
    key = derive_key(password)
    iv = os.urandom(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(data, BLOCK_SIZE))

def decrypt_data(data: bytes, password: str) -> bytes:
    try:
        key = derive_key(password)
        iv = data[:BLOCK_SIZE]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(data[BLOCK_SIZE:])
        return unpad(decrypted, BLOCK_SIZE)
    except Exception as e:
       
        return None


def encrypt_file(filepath: str, password: str):
    with open(filepath, 'rb') as f:
        plaintext = f.read()
    encrypted = encrypt_data(plaintext, password)
    with open(filepath, 'wb') as f:
        f.write(encrypted)

def decrypt_file(filepath: str, password: str):
    with open(filepath, 'rb') as f:
        encrypted = f.read()
    decrypted = decrypt_data(encrypted, password)
    with open(filepath, 'wb') as f:
        f.write(decrypted)
