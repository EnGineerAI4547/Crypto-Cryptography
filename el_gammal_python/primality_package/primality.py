import random
import sys
import os








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



