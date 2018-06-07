from __future__ import print_function

'''import numpy as np
from time import time

# Let's take the randomness out of random numbers (for reproducibility)
np.random.seed(0)

size = 4096
A, B = np.random.random((size, size)), np.random.random((size, size))
C, D = np.random.random((size * 128,)), np.random.random((size * 128,))
E = np.random.random((int(size / 2), int(size / 4)))
F = np.random.random((int(size / 2), int(size / 2)))
F = np.dot(F, F.T)
G = np.random.random((int(size / 2), int(size / 2)))

# Matrix multiplication
N = 20
t = time()
for i in range(N):
    np.dot(A, B)
delta = time() - t
print('Dotted two %dx%d matrices in %0.2f s.' % (size, size, delta / N))
del A, B

# Vector multiplication
N = 5000
t = time()
for i in range(N):
    np.dot(C, D)
delta = time() - t
print('Dotted two vectors of length %d in %0.2f ms.' % (size * 128, 1e3 * delta / N))
del C, D

# Singular Value Decomposition (SVD)
N = 3
t = time()
for i in range(N):
    np.linalg.svd(E, full_matrices = False)
delta = time() - t
print("SVD of a %dx%d matrix in %0.2f s." % (size / 2, size / 4, delta / N))
del E

# Cholesky Decomposition
N = 3
t = time()
for i in range(N):
    np.linalg.cholesky(F)
delta = time() - t
print("Cholesky decomposition of a %dx%d matrix in %0.2f s." % (size / 2, size / 2, delta / N))

# Eigendecomposition
t = time()
for i in range(N):
    np.linalg.eig(G)
delta = time() - t
print("Eigendecomposition of a %dx%d matrix in %0.2f s." % (size / 2, size / 2, delta / N))'''
import os
import sys
import timeit

import numpy
from numpy.random import random


def test_eigenvalue():
    """
    Test eigen value computation of a matrix
    """
    i = 500
    data = random((i, i))
    result = numpy.linalg.eig(data)


def test_svd():
    """
    Test single value decomposition of a matrix
    """
    i = 1000
    data = random((i, i))
    result = numpy.linalg.svd(data)
    result = numpy.linalg.svd(data, full_matrices=False)


def test_inv():
    """
    Test matrix inversion
    """
    i = 1000
    data = random((i, i))
    result = numpy.linalg.inv(data)


def test_det():
    """
    Test the computation of the matrix determinant
    """
    i = 1000
    data = random((i, i))
    result = numpy.linalg.det(data)


def test_dot():
    """
    Test the dot product
    """
    i = 10000
    a = random((i, i))
    b = numpy.linalg.inv(a)
    result = numpy.dot(a, b) - numpy.eye(i)

# Test to start. The dict is the value I had with the MKL using EPD 6.0 and without MKL using EPD 5.1

# Setting the following environment variable in the shell executing the script allows
# you limit the maximal number threads used for computation

