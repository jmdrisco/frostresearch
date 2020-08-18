# Matthew Mazzagatte
# Frost Research 2020
import numpy as np
import sys


"""Data Definition
    a pair is an object of the class Pair with:
    - in1 as a string of the first input
    - in2 as a string of the second input
    - out as a integer of 0 if the two inputs produce the same output or
      1 if the two inputs produce different output 
"""


class Pair:
    def __init__(self, in1: str, in2: str, out: int):
        self.in1 = in1
        self.in2 = in2
        self.out = out


def generate_binary(k: int) -> list:
    """ Takes an integer and returns a list with all binary numbers in the k dimension"""
    binaries = []
    i = 0

    while i < 2**k:
        if len(binaries) == 0:
            binaries.append("0"*k)
        elif i % 2 == 1:
            num = str(int(binaries[len(binaries)-1]) + 1)
            n = "0"*(k-len(num)) + num
            binaries.append(n)
        elif i % 2 == 0:
            num = str(int(binaries[len(binaries)-1])-1+10)
            n = "0"*(k-len(num)) + num
            if "2" in n:
                ind = n.index("2")
                if n[ind-1] != "1":
                    n = n[0:ind-1] + "1" + n[ind:]
                    n = n.replace("2"+"0"*(k-1-ind), "0"*(k-ind))
                else:
                    ind2 = 0
                    c = 0
                    a = n[0]
                    while a != "2":
                        c += 1
                        a = n[c]
                        if a == "0":
                            ind2 = c
                    n = n[0:ind2] + "1" + n[ind2+1:]
                    n = n[0:ind2+1] + "0"*(len(n[ind2:])-1)
            binaries.append(n)
        i += 1
    return binaries


def monomial_differences(in1: str, in2: str) -> str:
    """Takes two inputs and calculates the monomial difference between them"""

    monomial = ''
    for index in range(len(in1)):
        if in1[index] != in2[index]:
            x = "x" + str(index + 1)
            if monomial == '':
                monomial = monomial + x
            else:
                monomial = monomial + "*" + x
    return monomial


"""
citing source code for row_echelon():
Vasily Mitch (https://math.stackexchange.com/users/398967/vasily-mitch). 
    "How to reduce matrix into row echelon form in Python."
    https://math.stackexchange.com/q/3073117.

modified slightly for this algorithm
"""


def row_echelon(M: np.array) -> np.ndarray:
    """ Return Row Echelon Form of matrix A """

    # matrix is missing rows or columns, it is in row reduced form
    r, c = M.shape
    if r == 0 or c == 0:
        return M

    # we search for non-zero element in the first column
    for i in range(len(M)):
        if M[i, 0] != 0:
            break
    else:
        # if all elements in the first column are 0, we go to the next column
        B = row_echelon(M[:, 1:])
        # and then add the first zero-column back
        return np.hstack([M[:, :1], B])

    # if non-zero element happens not in the first row,
    # we switch rows
    if i > 0:
        ith_row = M[i].copy()
        M[i] = M[0]
        M[0] = ith_row

    # we add all subsequent rows with first row
    M[1:] = (M[1:] + M[0] * M[1:, 0:1]) % 2

    # we perform REF on matrix from second row, from second column
    B = row_echelon(M[1:, 1:])

    # we add first row and first (zero) column, and return
    return np.vstack([M[:1], np.hstack([M[1:, :1], B])])


def gauss(pairs: dict, first: str, second: str, k: int, inputs: list) -> bool:
    """Creates a matrix based on two inputs differing and determines whether
        the matrix is consistent or inconsistent"""

    n = len(inputs)
    mono = pairs[k].split("*")
    eqs = [Pair(first, second, 1)]

    # go through all pairs to find which ones produce univariate monomials
    # that are a part of the multivariate monomail
    for key in pairs.keys():
        if pairs[key] in mono:
            in1, in2 = key.split(",")[0], key.split(",")[1]
            eqs.append(Pair(in1, in2, 0))

    # generate matrix with the equations found above
    matrix = np.zeros((len(eqs), n + 1))
    for i in range(len(eqs)):
        col1 = inputs.index(eqs[i].in1)
        col2 = inputs.index(eqs[i].in2)
        matrix[i][col1] = 1.0
        matrix[i][col2] = 1.0
        matrix[i][n] = eqs[i].out

    # store matrix as np.array
    M = np.array(matrix, dtype='float')
    # print(M)
    M = row_echelon(M)
    # print(first, second, "\n", M)

    # go through the row-reduced matrix to determine if its consistent
    for row in M:
        # if it is inconsistent -> false
        if sum(row[0:len(row)-1]) == 0 and row[len(row)-1] == 1:
            return False
    return True


def main():

    if len(sys.argv) == 1:
        sys.exit("Please include the input file in the command line")
    else:
        with open(sys.argv[1], "r") as myfile:
            lines = myfile.readlines()
            input_lines = [line.strip() for line in lines if line.strip() != ""]
            for line in input_lines:
                for c in line:
                    if c.isalpha():
                        sys.exit("Reconfigure input file")

        # For each input, it runs the algorithm, calculating binary numbers
        # and determining which ones are in the input.
        for i in range(0, len(input_lines), 2):
            k = int(input_lines[i])
            binary = generate_binary(k)
            i = input_lines[i+1].split(",")
            inputs = [binary[int(x)] for x in i]
            print(inputs)

            # Store all the monomial difference between each input pair.
            pairs = {}
            for i in range(len(inputs)-1):
                for j in range(i+1, len(inputs)):
                    # print(i, j, monomial_differences(inputs[i], inputs[j]))
                    pairs[inputs[i] + "," + inputs[j]] = monomial_differences(inputs[i], inputs[j])
            t = True
            # Go through each pair
            for key in pairs.keys():
                # if the pair produces a multivariate monomial, we run our algorithm
                if "*" in pairs[key]:
                    # if the multivariate monomial can exist in the ideal without any
                    # of the univariate monomials in the ideal, then there is not a unique min-set
                    if gauss(pairs, key.split(",")[0], key.split(",")[1], key, inputs):
                        print("Does not produce a unique min-set")
                        t = False
                        break
            # We conclude the set of inputs produce a unique min-set if none failed above
            if t:
                print("Produces a unique min-set")


if __name__ == "__main__":
    main()
