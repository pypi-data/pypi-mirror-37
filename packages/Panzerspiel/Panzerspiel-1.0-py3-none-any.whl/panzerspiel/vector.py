import math


class vector():
    """
    The vector class is a small 2d vector class. Every mathematical operation
    is an independent function as pythons is not strictly oop orientated.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_int_tupel(self):
        return (int(self.x), int(self.y))

    def __str__(self):
        return str(self.x) + ", " + str(self.y)


def add(v1, v2):
    return vector(v1.x + v2.x, v1.y + v2.y)


def sub(v1, v2):
    return vector(v1.x - v2.x, v1.y - v2.y)


def div(v1, f):
    return vector(v1.x / f, v1.y / f)


def mul(v1, f):
    return vector(v1.x * f, v1.y * f)


def normalize(v1):
    length = math.sqrt(v1.x**2 + v1.y**2)
    v1.x = v1.x / length
    v1.y = v1.y / length
    return v1


def abs(v1):
    return math.sqrt(v1.x**2 + v1.y**2)


def polar(alpha, r):
    return mul(vector(math.cos(alpha), math.sin(alpha)), r)
