import math
import numpy as np


def deg2rad(angle):
    return angle * math.pi / 180


def rad2deg(angle):
    return angle * 180 / math.pi


def lin2db(value_lin):
    result = np.where(value_lin > 0.0000000001, value_lin, -10)
    np.log10(result, out=result, where=result > 0)
    return 20 * result


def db2lin(value_db):
    return 10 ** (value_db / 20)


def pow2db(value_pow):
    result = np.where(value_pow > 0.0000000001, value_pow, -10)
    np.log10(result, out=result, where=result > 0)
    return 10*result


def db2pow(value_db):
    return 10 ** (value_db / 10)


def cart2sph(x, y, z):
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    phi = np.arctan2(y, x)
    theta = np.arccos(z / r)
    return phi, theta, r


def sph2cart(phi, theta, r):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z
