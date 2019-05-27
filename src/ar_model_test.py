from ar_model import predict
import numpy as np


def __linear(x):
    return (8.3 * x) - 4


def __e(x):
    return 3 * np.exp(2*x) - 2


def __log(x):
    return -2.1 * np.log2(x)


def __poly_2(x):
    return 4 * (x**2) + 3.8


def __sin(x):
    return - np.sin(1 + 2*x) + 2