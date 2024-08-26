import secrets

class ECC:
    def __init__(self, p, a, b, G, n):
        """
        Initialize the ECC system.
        
        :param p: Prime number (finite field)
        :param a: Coefficient a of the elliptic curve
        :param b: Coefficient b of the elliptic curve
        :param G: Generator point (Gx, Gy)
        :param n: Order of the base point G
        """
        # Validate input types
        if not all(isinstance(i, int) for i in [p, a, b, n]):
            raise ValueError("p, a, b, and n must be integers.")
        if not isinstance(G, tuple) or len(G) != 2 or not all(isinstance(i, int) for i in G):
            raise ValueError("G must be a tuple of two integers.")
        
        self.p = p
        self.a = a
        self.b = b
        self.G = G
        self.n = n
        
        # Validate curve equation
        if (4 * a**3 + 27 * b**2) % p == 0:
            raise ValueError("Invalid curve: 4a^3 + 27b^2 must not be congruent to 0 mod p.")
        
        # Validate generator point
        if not self.is_on_curve(G):
            raise ValueError("The generator point G is not on the curve.")
    
    def is_on_curve(self, P):
        """
        Check if the point P lies on the elliptic curve.
        
        :param P: A point (x, y)
        :return: True if P lies on the curve, False otherwise
        """
        x, y = P
        return (y**2 - x**3 - self.a * x - self.b) % self.p == 0
    
    def point_addition(self, P, Q):
        """
        Perform point addition on the elliptic curve.
        
        :param P: Point P (x1, y1)
        :param Q: Point Q (x2, y2)
        :return: Resulting point R (x3, y3) from P + Q
        """
        if not self.is_on_curve(P) or not self.is_on_curve(Q):
            raise ValueError("Both points must lie on the curve.")
        
        if P == Q:
            return self.point_doubling(P)
        
        if P == (None, None):
            return Q
        if Q == (None, None):
            return P
        
        x1, y1 = P
        x2, y2 = Q
        
        if x1 == x2 and y1 != y2:
            return (None, None)  # Point at infinity
        
        if x1 == x2:
            return self.point_doubling(P)
        
        # Calculate the slope (lambda)
        slope = ((y2 - y1) * pow(x2 - x1, -1, self.p)) % self.p
        
        # Calculate x3 and y3
        x3 = (slope**2 - x1 - x2) % self.p
        y3 = (slope * (x1 - x3) - y1) % self.p
        
        return (x3, y3)
    
    def point_doubling(self, P):
        """
        Perform point doubling on the elliptic curve.
        
        :param P: Point P (x, y)
        :return: Resulting point R (x', y') from 2P
        """
        if not self.is_on_curve(P):
            raise ValueError("The point must lie on the curve.")
        
        x, y = P
        
        if y == 0:
            return (None, None)  # Point at infinity
        
        # Calculate the slope (lambda)
        slope = ((3 * x**2 + self.a) * pow(2 * y, -1, self.p)) % self.p
        
        # Calculate x' and y'
        x3 = (slope**2 - 2 * x) % self.p
        y3 = (slope * (x - x3) - y) % self.p
        
        return (x3, y3)
    
    def scalar_multiplication(self, k, P):
        """
        Perform scalar multiplication k * P on the elliptic curve.
        
        :param k: Scalar multiplier
        :param P: Point P (x, y)
        :return: Resulting point Q (x', y') from k * P
        """
        if not isinstance(k, int):
            raise ValueError("The scalar multiplier k must be an integer.")
        
        if k % self.n == 0 or not self.is_on_curve(P):
            return (None, None)  # Point at infinity
        
        result = (None, None)  # Point at infinity
        addend = P
        
        while k:
            if k & 1:
                result = self.point_addition(result, addend)
            addend = self.point_doubling(addend)
            k >>= 1
        
        return result
    
    def generate_private_key(self):
        """
        Generate a private key (a random integer).
        
        :return: Private key d
        """
        return secrets.randbelow(self.n)
    
    def generate_public_key(self, private_key):
        """
        Generate a public key corresponding to a given private key.
        
        :param private_key: The private key d
        :return: Public key Q (x, y)
        """
        if not isinstance(private_key, int):
            raise ValueError("Private key must be an integer.")
        
        if private_key <= 0 or private_key >= self.n:
            raise ValueError("Private key must be in the range [1, n-1].")
        
        return self.scalar_multiplication(private_key, self.G)

# Example parameters for secp256k1 (used in Bitcoin)
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0
b = 7
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Instantiate the ECC system
ecc = ECC(p, a, b, G, n)

# Generate keys
private_key = ecc.generate_private_key()
public_key = ecc.generate_public_key(private_key)

print("Private Key:", private_key)
print("Public Key:", public_key)