#include <iostream>
#include <stdexcept>
#include <tuple>
#include <random>
#include <cassert>

class ECC {
public:
    using Point = std::tuple<unsigned long long, unsigned long long>;

    ECC(unsigned long long p, unsigned long long a, unsigned long long b, Point G, unsigned long long n)
        : p(p), a(a), b(b), G(G), n(n) {
        // Validate curve equation
        if ((4 * a * a * a + 27 * b * b) % p == 0) {
            throw std::invalid_argument("Invalid curve: 4a^3 + 27b^2 must not be congruent to 0 mod p.");
        }

        // Validate generator point
        if (!isOnCurve(G)) {
            throw std::invalid_argument("The generator point G is not on the curve.");
        }
    }

    bool isOnCurve(Point P) const {
        auto [x, y] = P;
        return (y * y - (x * x * x + a * x + b)) % p == 0;
    }

    Point pointAddition(Point P, Point Q) const {
        if (!isOnCurve(P) || !isOnCurve(Q)) {
            throw std::invalid_argument("Both points must lie on the curve.");
        }

        auto [x1, y1] = P;
        auto [x2, y2] = Q;

        if (P == Q) {
            return pointDoubling(P);
        }

        if (x1 == x2 && y1 != y2) {
            return Point{0, 0};  // Point at infinity
        }

        if (x1 == x2) {
            return pointDoubling(P);
        }

        // Calculate the slope (lambda)
        unsigned long long slope = ((y2 - y1) * modInverse(x2 - x1, p)) % p;

        // Calculate x3 and y3
        unsigned long long x3 = (slope * slope - x1 - x2) % p;
        unsigned long long y3 = (slope * (x1 - x3) - y1) % p;

        return Point{x3, y3};
    }

    Point pointDoubling(Point P) const {
        if (!isOnCurve(P)) {
            throw std::invalid_argument("The point must lie on the curve.");
        }

        auto [x, y] = P;

        if (y == 0) {
            return Point{0, 0};  // Point at infinity
        }

        // Calculate the slope (lambda)
        unsigned long long slope = ((3 * x * x + a) * modInverse(2 * y, p)) % p;

        // Calculate x3 and y3
        unsigned long long x3 = (slope * slope - 2 * x) % p;
        unsigned long long y3 = (slope * (x - x3) - y) % p;

        return Point{x3, y3};
    }

    Point scalarMultiplication(unsigned long long k, Point P) const {
        if (k % n == 0 || !isOnCurve(P)) {
            return Point{0, 0};  // Point at infinity
        }

        Point result{0, 0};  // Point at infinity
        Point addend = P;

        while (k) {
            if (k & 1) {
                result = pointAddition(result, addend);
            }
            addend = pointDoubling(addend);
            k >>= 1;
        }

        return result;
    }

    unsigned long long generatePrivateKey() const {
        std::random_device rd;
        std::mt19937_64 eng(rd());
        std::uniform_int_distribution<unsigned long long> distr(1, n - 1);

        return distr(eng);
    }

    Point generatePublicKey(unsigned long long privateKey) const {
        if (privateKey <= 0 || privateKey >= n) {
            throw std::invalid_argument("Private key must be in the range [1, n-1].");
        }

        return scalarMultiplication(privateKey, G);
    }

private:
    unsigned long long p, a, b, n;
    Point G;

    unsigned long long modInverse(unsigned long long a, unsigned long long p) const {
        // Using Extended Euclidean Algorithm to find modular inverse
        unsigned long long m0 = p, t, q;
        unsigned long long x0 = 0, x1 = 1;

        if (p == 1)
            return 0;

        while (a > 1) {
            q = a / p;
            t = p;
            p = a % p;
            a = t;
            t = x0;
            x0 = x1 - q * x0;
            x1 = t;
        }

        if (x1 < 0)
            x1 += m0;

        return x1;
    }
};

int main() {
    // Example parameters for secp256k1 (used in Bitcoin)
    unsigned long long p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F;
    unsigned long long a = 0;
    unsigned long long b = 7;
    ECC::Point G = {0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 
                    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8};
    unsigned long long n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141;

    // Instantiate the ECC system
    ECC ecc(p, a, b, G, n);

    // Generate keys
    unsigned long long privateKey = ecc.generatePrivateKey();
    ECC::Point publicKey = ecc.generatePublicKey(privateKey);

    std::cout << "Private Key: " << privateKey << std::endl;
    std::cout << "Public Key: (" << std::get<0>(publicKey) << ", " << std::get<1>(publicKey) << ")" << std::endl;

    return 0;
}