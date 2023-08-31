from cryptography.hazmat.primitives import triple_des
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from os import urandom

def generate_key():
    # Generate a random 3DES key (168 bits)
    key = urandom(24)
    return key

def generate_iv():
    # Generate a random 8-byte IV
    iv = urandom(8)
    return iv

def encrypt(data, key, iv):
    # Encrypt data using 3DES
    backend = default_backend()
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    return encrypted_data

def decrypt(encrypted_data, key, iv):
    # Decrypt data using 3DES
    backend = default_backend()
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted_data

def main():
    # Example usage of Triple DES encryption and decryption
    key = generate_key()
    iv = generate_iv()
    data = b"Your plaintext data here"
    encrypted_data = encrypt(data, key, iv)
    print("Encrypted data:", encrypted_data)
    decrypted_data = decrypt(encrypted_data, key, iv)
    print("Decrypted data:", decrypted_data)

if __name__ == "__main__":
    main()
