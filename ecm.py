"""
My (David Hou's) really basic implementation of ECM
"""

import random

n = int(raw_input())

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return False, g
    else:
        return True, x % m

def add(x_p, y_p, x_q, y_q):
    inv = modinv((x_q - x_p) % n, n)
    if not inv[0]:
        return True, inv[1]
    l = ((y_q - y_p) * inv[1]) % n
    x_r = (l ** 2 - x_p - x_q) % n
    y_r = (l * (x_p - x_r) - y_p) % n
    return False, (x_r, y_r)

def double(x, y):
    inv = modinv(2 * y, n)
    if not inv[0]:
        return True, inv[1]
    l = 3 * x ** 2 * inv[1]
    x_r = (l ** 2 - 2 * x) % n
    y_r = (l * (x - x_r) - y) % n
    return False, (x_r % n, y_r % n)

def mult(x, y, f):
    x_w = x
    y_w = y
    for b in bin(f)[3:]:
        if b == '1':
            win, result = double(x_w, y_w)
            if win:
                return True, result % n
            win, result = add(result[0], result[1], x, y)
            if win:
                return True, result % n
            x_w, y_w = result
        else:
            win, result = double(x_w, y_w)
            if win:
                return True, result % n
            x_w, y_w = result
    return False, (x_w, y_w)

try:
    while n != 1:
        a = random.randint(1, n - 1)
        x = random.randint(1, n - 1)
        y = random.randint(1, n - 1)
        b = y ** 2 - x ** 3 - a * x

        for e in xrange(2, 21):
            win, result = mult(x, y, e)
            if win:
                if result == 0: break
                print "Found factor %d" % result
                n /= result
                break
            x, y = result
except (KeyboardInterrupt, SystemExit):
        print "Remaining factor: %d" % n
