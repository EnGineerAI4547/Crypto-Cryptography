# ElGamal Encryption and Decryption Algorithm

This is a Python implementation of the ElGamal encryption and decryption algorithm. ElGamal is a public-key cryptosystem that was proposed by Taher ElGamal in 1985. It is based on the discrete logarithm problem and is therefore considered to be secure against attacks by quantum computers.

## Introduction

The ElGamal cryptosystem is a public-key encryption scheme that relies on the difficulty of computing discrete logarithms in a finite cyclic group. The scheme is named after its inventor, Taher ElGamal. The algorithm consists of four main steps:

1. Key generation
2. Encryption
3. Decryption
4. Verification

In key generation, the algorithm generates a public-private key pair. The public key is used for encryption, while the private key is used for decryption. The encryption process involves transforming the plaintext message into a ciphertext that can only be decrypted with the private key. The decryption process reverses this transformation, recovering the original plaintext.

## Functions

This implementation includes the following functions:

- `generate_prime(n, primality_test="miller-rabin", k=10)`: Generates a random prime number of n bits using the specified primality test.
- `find_primitive_root(p)`: Finds a primitive root of a prime number p.
- `square_multiply(base, exponent, modulus)`: Computes base^exponent mod modulus using the square-and-multiply algorithm.
- `extended_euclidean_algorithm(a, b)`: Finds the greatest common divisor of two integers a and b using the extended Euclidean algorithm.
- `modular_inverse(a, modulus)`: Finds the modular inverse of an integer a modulo a given modulus using the extended Euclidean algorithm.
- `elgamal_encrypt(message, p, g, A)`: Encrypts a plaintext message using the ElGamal encryption algorithm.
- `elgamal_decrypt(ciphertext, p, a)`: Decrypts a ciphertext message using the ElGamal decryption algorithm.

## Dependencies

This implementation requires the following dependencies:

- Python 3.x
- NumPy

## Using VS Code

To use this implementation in Visual Studio Code, follow these steps:

1. Open the folder containing the implementation in Visual Studio Code.
2. Open a terminal window and navigate to the folder.
3. Run the command `python menu.py` to start the program.

## Implementation Details

The ElGamal implementation in this repository is written in Python and is intended to serve as an introduction to the algorithm. The key size is customizable, with the default recommended value of 2048 bits. The implementation uses the Miller-Rabin primality test to generate a random prime number, and the square-and-multiply algorithm for modular exponentiation.

The program can accept both integer and string inputs. If a string input is provided, it is first converted to a binary representation using the ASCII encoding, and then to a byte array for encryption. The program includes input validation for both the key size and message.

## Future Work

This implementation is intended as an introduction to ElGamal and can be used as a starting point for further development. One possible area for future work is to optimize the code to reduce the time complexity for larger input sizes. Another possible area for future work is to implement the algorithm in C, which would be faster and more efficient than the Python implementation.
