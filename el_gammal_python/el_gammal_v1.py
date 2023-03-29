""" ElGamal encryption and decryption functions """
""" Author: Eric Gonzalez 
    Date: Spring 2023
    Assignment 03
    Mehrdad Nojoumian
    CIS5371/CIS 4634: Practical Aspects of Modern Cryptography
"""



# Import the necessary modules
import  random 
from random import randint
from math import gcd, sqrt
import os
import re
import sys
import secrets






def menu():
    while True:
        print("\n\n\nPlease choose an option by selecting the corresponding number:")
        print("1. Learn about ElGamal encryption and decryption")
        print("2. Encrypt/Decrypt using ElGamal")
        print("3. Exit")
        choice = input("> ")
        
        if choice == "1":
            print("ElGamal is a public-key encryption algorithm based on the discrete logarithm problem in a finite field. It was proposed by Taher Elgamal in 1985.")
            print("The algorithm consists of a key generation phase, an encryption phase, and a decryption phase.")
            print("During key generation, the algorithm generates a public key and a private key.")
            print("The public key is used by anyone to encrypt messages intended for the owner of the private key.")
            print("The private key is kept secret by the owner and is used to decrypt messages encrypted with the corresponding public key.")
            print("During encryption, the message is divided into blocks, each of which is encrypted using a unique random number.")
            print("During decryption, each block is decrypted using the private key and the random number used to encrypt it.")
            print("This algorithm is secure as long as the discrete logarithm problem is computationally difficult.")
        elif choice == "2":
            run_elgamal()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please choose again.")






def square_multiply(base, exponent, modulus):
    """
    Computes (base^exponent) % modulus using the modular exponentiation algorithm.
    """


    result = 1
    base = base % modulus
    
    while exponent > 0:
        # If the current exponent bit is 1, multiply the result by the current base value
        if exponent % 2 == 1:
            result = (result * base) % modulus
        
        # Square the base and divide the exponent by 2
        base = (base * base) % modulus
        exponent = exponent // 2
    
    return result



class PrimalityChecker:
    def __init__(self):
        pass
    
    def is_fermat_prime(self, n, k=5):
        if n <= 1 or n == 4:
            return False
        elif n <= 3:
            return True
        else:
            for i in range(k):
                a = random.randint(2, n-2)
                if square_multiply(a, n-1, n) != 1:
                    return False
            return True
    
    def is_miller_rabin_prime(self, n, k=5):
        if n <= 1:
            return False
        elif n <= 3:
            return True
        elif n % 2 == 0:
            return False
        else:
            r = 0
            s = n - 1
            while s % 2 == 0:
                r += 1
                s //= 2
            
            for i in range(k):
                a = random.randint(2, n-2)
                x = square_multiply(a, s, n)
                if x == 1 or x == n-1:
                    continue
                for j in range(r-1):
                    x = square_multiply(x, 2, n)
                    if x == n-1:
                        break
                else:
                    return False
            return True
    
    def check_primality(self, n):
        while True:
            method = input("Which primality test would you like to use? (Fermat/Miller-Rabin): ").lower()
            if method == "fermat":
                return self.is_fermat_prime(n)
            elif method == "miller-rabin":
                return self.is_miller_rabin_prime(n)
            else:
                print("Invalid method. Please choose either Fermat or Miller-Rabin.")


# Function to generate a random prime number using either the Fermat or Miller-Rabin primality test
# It uses the PrimalityChecker class functions within its implementation
# Parameters:
#   n: int - length of the prime number in bits
#   k: int - number of iterations for the primality test
#   primality_test: str - which primality test to use (fermat or miller-rabin)
# Returns:
#   int - a random prime number
# 
# Note: This function is not part of the PrimalityChecker class definition
def generate_prime(n, k=5, primality_test="miller-rabin"):
    primality_checker = PrimalityChecker()
    
    while True:
        p = bytearray(n//8)
        p[-1] |= 1
        p[0] |= 128
        for i in range(1, n//8 - 1):
            p[i] = randint(0, 255)
        if primality_test == "fermat" and primality_checker.is_fermat_prime(int.from_bytes(p, 'big'), k):
            return int.from_bytes(p, 'big')
        elif primality_test == "miller-rabin" and primality_checker.is_miller_rabin_prime(int.from_bytes(p, 'big'), k):
            return int.from_bytes(p, 'big')


# Define a function to find a primitive root modulo p.
def find_primitive_root(p):
    if p == 2:
        return 1
    p1 = 2
    p2 = (p - 1) // p1
    while True:
        g = random.randint(2, p-1)
        if not (pow(g, (p-1)//p1, p) == 1):
            if not pow(g, (p-1)//p2, p) == 1:
                return g
            



#Define a function to call extended euclidean algorithm

def extended_euclidean_algorithm(a, b):
    """
    Compute the greatest common divisor (GCD) of two integers a and b, as well as the
    coefficients x and y such that a*x + b*y = gcd(a, b).
    """
    # Base case: if b is 0, then gcd(a, b) = a, x = 1, and y = 0
    if b == 0:
        return a, 1, 0
    
    # Recursive step: compute the GCD and coefficients for b and a % b
    gcd, x1, y1 = extended_euclidean_algorithm(b, a % b)
    
    # Use the result of the recursive step to compute the GCD and coefficients for a and b
    x = y1
    y = x1 - (a // b) * y1
    
    return gcd, x, y


#Define a function to call elgamal encryption

# ElGamal encryption algorithm
def elgamal_encrypt(plaintext, p, g, A):
    """
    Encrypt a plaintext using ElGamal encryption algorithm.
    """
    k = random.randint(1, p-2)
    while gcd(k, p-1) != 1:
        k = random.randint(1, p-2)
    
    C1 = pow(g, k, p)
    C2 = plaintext * pow(A, k, p) % p
    return (C1, C2)

# Define a function to call elgamal decryption


# ElGamal decryption algorithm
def elgamal_decrypt(ciphertext, p, a):
    """
    Decrypt a ciphertext using ElGamal decryption algorithm.
    """
    C1, C2 = ciphertext
    D = pow(C1, a, p)
    D_inv = extended_euclidean_algorithm(D, p)[1] % p
    plaintext = C2 * D_inv % p
    return plaintext



def run_elgamal():
    print("Running ElGamal encryption and decryption algorithm...")

    # Input validation for number of bits
    while True:
        try:
            n = int(input("Enter the number of bits for the prime number (recommended value: 2048): "))
            if n <= 0:
                print("Please enter a positive integer.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    # Generate prime number with Miller-Rabin primality test
    primality_checker = PrimalityChecker()
    p = generate_prime(n, primality_test="miller-rabin", k=10)
    g = find_primitive_root(p)
    a = randint(1, p-2)
    A = square_multiply(g, a, p)
    print(f"p: {p}")
    print(f"g: {g}")
    print(f"a: {a}")
    print(f"A: {A}")

    # Input validation for message
    while True:
        message = input("Enter the message to encrypt: ")
        if message.isnumeric():
            message = int(message)
            if message >= p or message < 0:
                print(f"Message must be an integer less than p ({p}).")
                continue
            break
        else:
            try:
                # Convert the string to binary and then to a byte array
                binary_message = ''.join(format(ord(c), '08b') for c in message)
                message_bytes = bytearray(int(binary_message[i:i+8], 2) for i in range(0, len(binary_message), 8))
                break
            except ValueError:
                print("Please enter a valid message.")

    if isinstance(message, int):
        # Encrypt the message
        ciphertext = elgamal_encrypt(message, p, g, A)
    else:
        # Encrypt the message byte array
        if len(message_bytes) > (p.bit_length() - 1) // 8:
            print("WARNING: Message is too long to be encrypted securely.")
        ciphertext = [elgamal_encrypt(byte, p, g, A) for byte in message_bytes]

    print(f"This is the encrypted message also known as ciphertext: {ciphertext}")

    if isinstance(message, int):
        # Decrypt the message
        plaintext = elgamal_decrypt(ciphertext, p, a)
    else:
        # Decrypt the message byte array
        plaintext = b''.join(bytes([elgamal_decrypt(byte, p, a)]) for byte in ciphertext).decode()

    print(f"\nThe decrypted plaintext is: {plaintext}")




menu()