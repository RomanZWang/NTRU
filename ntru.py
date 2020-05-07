import math
import random
import itertools
import numpy as np
from numpy.fft import rfft, irfft, multiply, prod
from sympy import GF, invert
from sympy.abc import x
from sympy import ZZ, QQ, FF, Poly
from sympy import intt, ntt, fft, ifft, simplify
from sympy.polys import polytools

def is_prime(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def gcd(p, q):
    if p is 0:
        return q
    return gcd(q%p,p)

def find_inverse(p, m):
    if p % m == 1:
        return 1
    for candidate in range(2, m):
        # print((p*candidate) % m)
        if (p*candidate) % m == 1:
            return candidate
    raise Exception("no inverse found")
    print("No inverse found")
    return False

def get_coprime(p_range, q_range):
    for p_candidate in p_range:
        for q_candidate in q_range:
            if gcd(p_candidate, q_candidate) == 1:
                yield p_candidate, q_candidate

MOD = Poly(x**N-1,x).set_domain(ZZ)

def apply_dual_modulus(expression, q, N):
    return expression.trunc(q) % MOD

def generate_polynomial(N, d=13, neg_ones_diff=1):

    def random_poly(length, d, neg_ones_diff):
        return Poly(np.random.permutation(
            np.concatenate((np.zeros(length - 2 * d - neg_ones_diff), np.ones(d), -np.ones(d + neg_ones_diff)))),
            x).set_domain(ZZ)
    yield random_poly(N, d, neg_ones_diff)

def invert_polynomial(f_polynomial, N, p):
    modulus_polynomial=MOD
    return invert(f_polynomial, modulus_polynomial, domain=GF(p))

def invert_poly(f_poly, N, p):
    R_poly = MOD
    inv_poly = None
    if is_prime(p):
        log.debug("Inverting as p={} is prime".format(p))
        inv_poly = invert(f_poly, R_poly, domain=GF(p))
    elif is_2_power(p):
        log.debug("Inverting as p={} is 2 power".format(p))
        inv_poly = invert(f_poly, R_poly, domain=GF(2))
        e = int(math.log(p, 2))
        for i in range(1, e):
            log.debug("Inversion({}): {}".format(i, inv_poly))
            inv_poly = ((2 * inv_poly - f_poly * inv_poly ** 2) % R_poly).trunc(p)

def generate_parameters(N_range=range(250, 2500), p_range=range(250, 2500), q_range=range(3, 4)):
    # Generate p, q, N such that
    # N is a a large prime representing the degree of our modulo for our residue class
    # p is a small prime modulus coprime to q
    # q is a large modulus coprime to p

    # Todo: enforce N > q >> p

    ATTEMPTS = 100

    def sample_range(number_range, looking_for_prime=True):
        if looking_for_prime:
            for candidate_prime in number_range:
                if is_prime(candidate_prime):
                    return candidate_prime
            raise ValueError("no primes found in defined range")
        else:
            return random.choice(number_range)

    def get_coprime(p_range, q_range):
        for p_candidate in p_range:
            for q_candidate in q_range:
                if gcd(p_candidate, q_candidate) == 1:
                    yield p_candidate, q_candidate

    def get_f_g_h(p, q, N):
        current_attempt=0
        for f in generate_polynomial(N):
            current_attempt +=1
            if current_attempt>=ATTEMPTS:
                break
            #f = next(generate_polynomial(N))
            print("Candidate")
            print(f)
            try:
                f_p = invert_polynomial(f, N, p)
            except:
                continue
            try:
                f_q = invert_polynomial(f, N, q)
            except:
                continue
            g = next(generate_polynomial(N))
            h = (p*f_q*g).trunc(q)
            return f, f_p, f_q, g, h
        raise Exception("Cannot find invertible f")

    N = sample_range(N_range, looking_for_prime=True)
    f = None
    for p, q in get_coprime(p_range, q_range):
        try:
            f, f_p, f_q, g, h = get_f_g_h(p, q, N)
            if f is not None:
                return p, q, f, f_p, f_q, g, h
        except:
            pass
    raise Exception("invertible f not found")
