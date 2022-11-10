from __future__ import division
from sage.all import *
from copy import copy, deepcopy
from sage.rings.polynomial.pbori.pbori import *
from sage.rings.polynomial.pbori import *
from random import randint
import sys
from sage.sat.boolean_polynomials import solve as solve_sat
import logging

# create logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

def SingleMatrix( X, r0, r1 ):
    Y = []
    for i in range(64):
        Y.append( X[i] + X[( i + (64 - r0) ) % 64] + X[ ( i + (64 - r1) ) % 64 ] )
    return Y
        

def Matrix( X ):
    X[0  :64]  = SingleMatrix(X[0  : 64], 19, 28 )
    X[64 :128] = SingleMatrix(X[64 :128], 61, 39 )
    X[128:192] = SingleMatrix(X[128:192], 1,  6 )
    X[192:256] = SingleMatrix(X[192:256], 10, 17 )
    X[256:320] = SingleMatrix(X[256:320], 7, 41 )

    return X

def SingleSbox( y0, y1, y2, y3, y4 ):
    x0 = y4*y1 + y3 + y2*y1 + y2 + y1*y0 + y1 + y0
    x1 = y4 + y3*y2 + y3*y1 + y3 + y2*y1 + y2 + y1 + y0
    x2 = y4*y3 + y4 + y2 + y1 + 1
    x3 = y4*y0 + y4 + y3*y0 + y3 + y2 + y1 + y0
    x4 = y4*y1 + y4 + y3 + y1*y0 + y1
    return x0, x1, x2, x3, x4

def Sbox( Y ):
    Z = [ R(0) for i in range(320)]
    for j in range(64):
        Z[0 + j], Z[64 + j], Z[128 + j], Z[192 + j] , Z[256 + j] = SingleSbox( Y[0 + j], Y[64 + j], Y[128 + j], Y[192 + j], Y[256+j] )
    return Z

def addConst ( X, r ):
    constant = [ 0xf0, 0xe1, 0xd2, 0xc3, 0xb4, 0xa5, 0x96, 0x87, 0x78, 0x69,
            0x5a, 0x4b ]
    base = 184

    for i in range(8):
        if constant[r] >> ( 7 - i ) & 0x1:
            X[ base + i] += 1

    return X

if __name__ == '__main__':
    ROUNDS = 4
    R = declare_ring( [ Block( 'x', (2*ROUNDS - 1)*320 ),'u' ], globals() )
    X = [R(x(i)) for i in range(320)]
    a_vars  = [[R(x(320*(2*r + 1) + i)) for i in range(320)] for r in range(ROUNDS -1)]
    b_vars  = [[R(x(320*(2*r + 2) + i)) for i in range (320)] for r in range(ROUNDS -1)]          
    diff = [[0] * 320 for i in range(2)]
    diff[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
    diff[1] = [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
    for i in range(64):
        X[i] += diff[0][i] * R(u)
    Q = set()
    for r in range(0,ROUNDS-1): 
        X = addConst(X,r)
        X = Sbox(X)
        for i in range( 320 ):
            a = X[i] / R(u)
            b = X[i] + a * R(u)
            # the r th round, the i th variable
            # x = a * u + b
            Q.add(a + a_vars[r][i])
            Q.add(b + b_vars[r][i])
            X[i] = a_vars[r][i] * R(u) + b_vars[r][i]
       
        X = Matrix( X )
    
    X = addConst(X,ROUNDS-1)
    X = Sbox(X)
    for i in range(320):
        Q.add(X[i]/ R(u) + diff[1][i])
    for q in Q:
        print(q)