import math


def intsign(i):
    if abs(i) != i:
        return -1
    else:
        return 1


def fib_gen():
    k0 = k1 = p = 1
    while True:
        p = k0 + k1
        k0 = k1
        k1 = p
        yield p


def alt_sign_gen():
    i = -1
    while True:
        i *= -1
        yield i


def numerate_gen():
    i = 0
    while True:
        i += 1
        yield i


def ceil_exp(i, e):
    if i == 0:
        return 0
    return 2**math.ceil(math.log(i, e))


def floor_exp(i, e):
    if i == 0:
        return 0
    return 2**math.floor(math.log(i, e))
