from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Util import Counter

class AESCrypto:
    MODE_CBC = 'CBC'
    MODE_CFB = 'CFB'
    MODE_OFB = 'OFB'
    MODE_CTR = 'CTR'

    def __init__(self, key, mode=MODE_CBC):
        self.key = key
        self.mode = mode

    def get_cipher(self, iv=None):
        if self.mode == self.MODE_CBC:
            return AES.new(self.key, AES.MODE_CBC, iv)
        elif self.mode == self.MODE_CFB:
            return AES.new(self.key, AES.MODE_CFB, iv)
        elif self.mode == self.MODE_OFB:
            return AES.new(self.key, AES.MODE_OFB, iv)
        elif self.mode == self.MODE_CTR:
            ctr = Counter.new(128)
            return AES.new(self.key, AES.MODE_CTR, counter=ctr)
        else:
            raise ValueError("Unsupported mode")

    def encrypt(self, plaintext):
        iv = get_random_bytes(AES.block_size) if self.mode != self.MODE_CTR else b''
        cipher = self.get_cipher(iv)
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return iv + ciphertext

    def decrypt(self, ciphertext):
        iv_length = AES.block_size if self.mode != self.MODE_CTR else 0
        iv = ciphertext[:iv_length]
        cipher = self.get_cipher(iv)
        decrypted = unpad(cipher.decrypt(ciphertext[iv_length:]), AES.block_size)
        return decrypted.decode()

if __name__ == "__main__":
    key = get_random_bytes(32)  # Use a 256-bit key
    plaintext = "YourPlainTextHere"
    
    for mode in [AESCrypto.MODE_CBC, AESCrypto.MODE_CFB, AESCrypto.MODE_OFB, AESCrypto.MODE_CTR]:
        print(f"Mode: {mode}")
        aes = AESCrypto(key, mode)
        ciphertext = aes.encrypt(plaintext)
        print("Ciphertext:", ciphertext)
        decrypted_text = aes.decrypt(ciphertext)
        print("Decrypted text:", decrypted_text)
        print("-" * 50)
