import math
from sympy import GF, invert
import logging
import numpy as np
from sympy.abc import x
from sympy import ZZ, Poly

def is_prime(n):
    if n<=1:
        return False
    if n==2 or n==3:
        return True
    if n%2 == 0 or n%3 == 0:
        return False
    for candidate in range(6, int(math.floor(math.sqrt(n))), 6):
        if n%(candidate-1) == 0 or n%(candidate+1) == 0:
            return False
    return True

# TODO: Refactor
def is_2_power(n):
    return n != 0 and (n & (n - 1) == 0)

# TODO: Refactor
def random_poly(length, d, neg_ones_diff=0):
    return Poly(np.random.permutation(
        np.concatenate((np.zeros(length - 2 * d - neg_ones_diff), np.ones(d), -np.ones(d + neg_ones_diff)))),
        x).set_domain(ZZ)

# TODO: Refactor
def invert_poly(f_poly, R_poly, p):
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
    else:
        raise Exception("Cannot invert polynomial in Z_{}".format(p))
    log.debug("Inversion: {}".format(inv_poly))
    return inv_poly

if __name__ == "__main__":
    print("Hello")
