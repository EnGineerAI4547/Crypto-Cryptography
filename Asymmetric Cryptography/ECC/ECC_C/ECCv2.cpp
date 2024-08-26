#include <iostream>
#include <stdexcept>
#include <tuple>
#include <random>
#include <unordered_map>
#include <string>

class ECC {
public:
    using Point = std::tuple<unsigned long long, unsigned long long>;

    // Predefined curves
    static const std::unordered_map<std::string, ECC> predefined_curves;

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

    static ECC selectCurve(const std::string& curve_name) {
        auto it = predefined_curves.find(curve_name);
        if (it == predefined_curves.end()) {
            throw std::invalid_argument("Invalid curve name. Available curves are: secp256k1, secp192k1");
        }
        return it->second;
    }

    bool isOnCurve(Point P) const {
        auto [x, y] = P;
        return (y * y - (x * x * x + a * x + b)) % p == 0;
    }

    Point pointAddition(Point P, Point Q) const {
        // Same as before
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
        // Same as before
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
        // Same as before
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
        // Same as before
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

// Define the predefined curves
const std::unordered_map<std::string, ECC> ECC::predefined_curves = {
    {"secp256k1", ECC(
        0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
        0,
        7,
        ECC::Point(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 
                   0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8),
        0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    )},
    {"secp192k1", ECC(
        0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFEE37,
        0,
        3,
        ECC::Point(0xDB4FF10EC057E9AE26B07D028DDBF2CDB0E42A1C139EA0F4FF2A50A5EEC59C80,
                   0x9B2F2F6D9C5628A784416A2F7EC3E821A0D51DEAEFF52A29A1AD77F6A38E8E74),
        0xFFFFFFFFFFFFFFFFFFFFFFFE26F2FC170F69466A74DEFD8D
    )}
};

int main() {
    try {
        // Select a curve by name
        ECC ecc = ECC::selectCurve("secp256k1");

        // Generate keys
        unsigned long long privateKey = ecc.generatePrivateKey();
        ECC::Point publicKey = ecc.generatePublicKey(privateKey);

        std::cout << "Private Key: " << privateKey << std::endl;
        std::cout << "Public Key: (" << std::get<0>(publicKey) << ", " << std::get<1>(publicKey) << ")" << std::endl;
    } catch (const std::invalid_argument& e) {
        std::cerr << e.what() << std::endl;
    }

    return 0;
}