import os
import keyring
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import argparse


SERVICE_NAME = "EncryptionSoftware"
USERNAME = "EnkripcijskiKljuc"

def process_CMD():
    parser = argparse.ArgumentParser()
    parser.add_argument("-enc", "--encrypt", help = "Show Output")
    parser.add_argument("-dec", "--decrypt", help = "Show Output")
    parser.add_argument("-f", "--file", help = "Show Output")
    args = parser.parse_args()
    
    if args.Output:
        print("Displaying Output as: % s" % args.Output)

def encrypt_file(file_path):
    key = keyring.get_password(SERVICE_NAME, USERNAME)
    if key is None:
        key = os.urandom(32)  # AES-256 key
        keyring.set_password(SERVICE_NAME, USERNAME, key.hex())
    else:
        key = bytes.fromhex(key)
        
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
    key = keyring.get_password(SERVICE_NAME, USERNAME)
    if key is None:
        key = os.urandom(32)  # AES-256 key
        keyring.set_password(SERVICE_NAME, USERNAME, key.hex())
    else:
        key = bytes.fromhex(key)
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


encryptedFIle = encrypt_file(file_path)

    
    
