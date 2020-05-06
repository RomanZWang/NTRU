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
