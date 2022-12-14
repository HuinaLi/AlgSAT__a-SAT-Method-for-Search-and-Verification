import sys
import math

ROUNDS = 3
# numvars
    # a_vars[0]      v 1    -  1600
    # a_vars[1]      v 1601 -  3200
    # a_vars[2]      v 3201 -  4800
    # a_vars[3]      v 4801 -  6400
    # a_vars[4]      v 6401 -  8000
    # a_vars[5]      v 8001 -  9600
    # b_vars[0]      v 9601 -  11200
    # b_vars[1]      v 11201 - 12800
    # b_vars[2]      v 12801 - 14400
    # b_vars[3]      v 14401 - 16000
    # b_vars[4]      v 16001 - 17600
    # b_vars[5]      v 17601 - 19200
    
# keccak_sbox 29 clauses  
cnf_chi = [
    [4, -9, -10],
    [-4, 9, -10],
    [-1, 6, -7],
    [-2, 7, -8],
    [3, -8, -9],
    [-5, -6, 10],
    [1, -6, -7],
    [-1, 4, 5, 9],
    [-2, 4, 7],
    [1, 2, -3, 6],
    [2, 4, -7],
    [3, 5, -8],
    [-3, 5, 8],
    [2, -5, 10],
    [1, 4, -9],
    [1, -4, 9],
    [2, -4, 7, 8],
    [2, 5, -10],
    [1, 3, -6],
    [-2, -5, 6, -10],
    [-3, 8, -9],
    [-1, 2, -3, -6],
    [-1, -4, 5, -9],
    [3, -5, 8, 9],
    [-3, -5, -8, 9],
    [-2, 5, 6, 10],
    [-1, 6, 8, 10],
    [-2, -4, -7, 8],
    [-1, 4, 6, -8, -10]
]
row = [0]*10
for r in range(ROUNDS): 
    for y in range (5):
        for z in range (64):   
            # a_vars
            #row = [2*r*1600+(z+320*y),2*r*1600+64+z+320*y,2*r*1600+128+z+320*y,2*r*1600+192+z+320*y,2*r*1600+256+z+320*y,(2*r+1)*1600+z+320*y,(2*r+1)*1600+64+z+320*y,(2*r+1)*1600+128+z+320*y,(2*r+1)*1600+192+z+320*y,(2*r+1)*1600+256+z+320*y]
            # b_vars
            row = [2*r*1600+9600+(z+320*y),2*r*1600+9600+64+z+320*y,2*r*1600+9600+128+z+320*y,2*r*1600+9600+192+z+320*y,2*r*1600+9600+256+z+320*y,(2*r+1)*1600+9600+z+320*y,(2*r+1)*1600+9600+64+z+320*y,(2*r+1)*1600+9600+128+z+320*y,(2*r+1)*1600+9600+192+z+320*y,(2*r+1)*1600+9600+256+z+320*y]
            
            for i in range (len(cnf_chi)):
                CNF_clause= ""
                for j in range(len(cnf_chi[i])):
                    temp = int(cnf_chi[i][j])
                    if temp > 0 :
                        CNF_clause += str(row[ temp-1] + 1) + " "
                    else:
                        CNF_clause += str(-1 * row[abs(temp+1)]-1) + " "
                CNF_clause += '0'
                print(CNF_clause)
                

"""
for i in range (len(cnf_chi)):
    out= ""
    for j in range(len(cnf_chi[i])):
        out += str(cnf_chi[i][j]) + " "
    out += '0' 
    print('\n')
    print(out)
"""