
# Assignment 02 - Implementing the DES Algorithm

This project was created for **Assignment 02** given by Professor Mehrdad Nojoumian with the class name being CIS5371/CIS 4634: Practical Aspects of Modern Cryptography. The objective of this project was to implement the Data Encryption Standard (DES) algorithm for the purpose of exposing us to one of the most widely used symmetric/public key encryption techniques until the advent of AES. 

DES is a symmetric-key block cipher that was developed by IBM in the 1970s as an encryption standard for the US government. It uses a 56-bit key to encrypt data in blocks of 64 bits. Although DES has been replaced by more advanced encryption standards, it is still widely used in certain applications and is a crucial part of the history of cryptography. 

As part of this project, I decided to implement DES using Python. However, I have future plans to also implement it in C as well. Additionally, I plan to implement a GUI for the DES algorithm and explore other encryption techniques. 

This project was a challenging yet rewarding experience, and I believe that the technical difficulty of DES is good preparation for the field of cryptography. Implementing DES has enabled me to better understand other encryption techniques and their underlying principles.This project is designed to be very user-friendly, requiring no installations or dependencies beyond what is included in the code at the top. Although the code is currently written in a single file, there are plans to create modules for the functions and further efforts to create classes to make the code even more modular.

The project is simple to use and will guide the user through each step with clear prompts in the terminal. Multiple explanations were carefully crafted to guide the user, assuming zero knowledge of cryptography. This project is ideal for users who want to learn about key cryptography topics via an interactive menu.

Additionally, users who want to skip the learning process and go directly to encrypting or decrypting can do so by clicking the appropriate menu response on the terminal. Overall, this project aims to be both accessible and informative for users of all levels of expertise in cryptography.


## `readfile` function

This function reads data from a file and returns it as plaintext or ciphertext, depending on the selected mode.

**Warning:** The double DES and triple DES functionality is still a work in progress. We apologize for any inconvenience this may cause.

For single DES, everything is working great! However, if users elect to select their private keys themselves instead of having them generated automatically, they will need to remember their keys. 

If users elect to have the private key generated, they must copy it from the terminal when they go to decrypt the ciphertext. Similarly, they will have to write down or copy the ciphertext/plaintext from the terminal depending on which functionality they wish to do because it will be necessary to reverse the process. 

**Warning:** We are working on implementing other modes of operation, including:

- CBC (Cipher Block Chaining) mode: This mode uses the output of the previous block to encrypt the current block, making it more secure than ECB mode.
- CFB (Cipher Feedback) mode: This mode turns a block cipher into a stream cipher by encrypting the previous ciphertext block instead of the plaintext block.
- OFB (Output Feedback) mode: This mode also turns a block cipher into a stream cipher, but uses the previous keystream block instead of the previous ciphertext block.
- CTR (Counter) mode: This mode turns a block cipher into a stream cipher by using a counter as the input to the encryption algorithm.

Please note that the functionality for these modes is currently in the works and may not work as expected. We appreciate your patience as we continue to improve our DES implementation.
