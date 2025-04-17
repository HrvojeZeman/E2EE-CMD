
import os
import keyring
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import tkinter as tk
from tkinter import filedialog

SERVICE_NAME = "EncryptionSoftware"
USERNAME = "EnkripcijskiKljuc"

def get_or_create_key():
    key = keyring.get_password(SERVICE_NAME, USERNAME)
    if key is None:
        key = os.urandom(32)  # AES-256 key
        keyring.set_password(SERVICE_NAME, USERNAME, key.hex())
    else:
        key = bytes.fromhex(key)
    return key

def encrypt_file(file_path):
    key = get_or_create_key()
    InitilaisationVector = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(InitilaisationVector), backend=default_backend())
    encryptor = cipher.encryptor()
    
    with open(file_path, "rb") as f:
        data = f.read()
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    with open(file_path + ".enc", "wb") as f:
        f.write(InitilaisationVector + encrypted_data)
    
    print(f"File encrypted successfully: {file_path}.enc")

def decrypt_file(encrypted_path):
    key = get_or_create_key()
    
    with open(encrypted_path, "rb") as f:
        iv = f.read(16)
        encrypted_data = f.read()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()
    
    original_path = encrypted_path.replace(".enc", "_decrypted")
    with open(original_path, "wb") as f:
        f.write(decrypted_data)
    
    print(f"File decrypted successfully: {original_path}")
    
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
print(file_path)

encryptedFIle = encrypt_file(file_path)

    
    
