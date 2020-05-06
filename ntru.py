import math
import numpy as np
from sympy import GF, invert
from sympy.abc import x
from sympy import ZZ, QQ, FF, Poly
import random

def is_prime(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_power_of_two(n):
    return n != 0 and (n & (n - 1) == 0)

def gcd(p, q):
    if p is 0:
        return q
    return gcd(q%p,p)

### Parameter generation
# Generate f, g
# Generate N, p, q
# Check invertibility of f mod p, q
# Create h from p, f, g

def generate_polynomial(N):
    coefficients = random.choices([-1, 0, 1], k=N-1)
    return Poly(coefficients, x).set_domain(ZZ)

def invert_polynomial(f_polynomial, N, p):
    modulus_polynomial=Poly(x**N-1,x).set_domain(ZZ)
    return invert(f_polynomial, modulus_polynomial, domain=GF(p))

def generate_parameters(N_range=range(250, 2500), p_range=range(250, 2500), q_range=range(3, 4)):
    # Generate p, q, N such that
    # N is a a large prime representing the degree of our modulo for our residue class
    # p is a small prime modulus coprime to q
    # q is a large modulus coprime to p

    # Todo: enforce N > q >> p

    ATTEMPTS = 1000

    def sample_range(number_range, looking_for_prime=True):
        if looking_for_prime:
            for candidate_prime in number_range:
                if is_prime(candidate_prime):
                    return candidate_prime
            raise ValueError("no primes found in defined range")
        else:
            return random.choice(number_range)

    def get_coprime(p_range, q_range):
        p = None
        q = None
        for p_candidate in p_range:
            if is_prime(p_candidate):
                p = p_candidate
                break
        for q_candidate in q_range:
            if is_prime(q_candidate):
                q = q_candidate
                break
        if p is not None and q is not None:
            return p, q
        raise Exception("Cannot find coprime p, q")

    def get_f_g_h(p, q, N):
        for iterations in range(ATTEMPTS):
            f = generate_polynomial(N)

            try:
                f_p = invert_polynomial(f, N, p)
            except:
                continue
            try:
                f_q = invert_polynomial(f, N, q)
            except:
                continue
            g = generate_polynomial(N)
            h = (p*f_q*g).trunc(q)
            return f, f_p, f_q, g, h
        raise Exception("Cannot find invertible f")

    N = sample_range(N_range, looking_for_prime=True)
    p, q = get_coprime(p_range, q_range)
    f, f_p, f_q, g, h = get_f_g_h(p, q, N)
    return p, q, f, f_p, f_q, g, h

def apply_dual_modulus(expression, q, N):
    return expression.trunc(q) % N
