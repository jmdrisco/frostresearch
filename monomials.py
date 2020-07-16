from itertools import combinations


# generates all binary inputs
def recursive(arr, mono, k):
    if len(mono) == k:
        arr.append(mono)
        return arr

    mono1 = "0" + mono
    arr = recursive(arr, mono1, k)

    mono2 = "1" + mono
    arr = recursive(arr, mono2, k)
    return arr

# puts all possible outputs with each input
# ex. [[0,0], 0]  &  [[0,0], 1]
def create_outputs(monos):
    outs = []
    for mono in monos:
        new_mono = [int(x) for x in mono]
        outs.append([new_mono, 0])
        outs.append([new_mono, 1])
    return outs

# returns all possible combinations of I/O pairs
def create_inputs(pairs, k):
    combos = []
    for i in range(2, 2**k+1):
        perms = combinations(pairs, i)
        for perm in list(perms):
            app = True
            vals = []
            opp = []
            for val in perm:
                if val[0] in vals:
                    app = False
                else:
                    vals.append(val[0])
                opp.append([val[0], (val[1]+1) % 2])
            if app and tuple(opp) not in combos:
                combos.append(perm)
    return combos

# in_out_pairs is a list of lists with input-output pairs: [[input_1, output_1],[input_2, output_2]]
# takes in_out_pairs and returns a list of monomials to put into M2
def create_mono(in_out_pairs):
    monomials = []
    # compare each output
    for index in range(len(in_out_pairs) - 1):
        pair_1 = in_out_pairs[index]

        for index_2 in range(index + 1, len(in_out_pairs)):
            pair_2 = in_out_pairs[index_2]

            # if outputs are different, create a monomial
            if pair_1[1] != pair_2[1]:
                monomial = find_differences(pair_1[0], pair_2[0])

                # if monomial is not in monomials, add to overall list
                if monomial not in monomials:
                    monomials.append(monomial)
    return monomials


def find_differences(data_1, data_2):
    monomial = ''
    for index in range(len(data_1)):
        if data_1[index] != data_2[index]:
            x = "x" + str(index + 1)
            if monomial == '':
                monomial = monomial + x
            else:
                monomial = monomial + "*" + x
    return monomial


def main():
    # define k
    k = 2
    start = ""
    monomials = recursive([], start, k)
    outs = create_outputs(monomials)
    inputs = create_inputs(outs, k)

    #reformats the I/O pairs
    inputs = [list(inp) for inp in inputs]
    ideals = []
    for inp in inputs:
        ideals.append(create_mono(inp))
    for i in range(len(ideals)):
        print(inputs[i], "-->", ideals[i])
    print(len(ideals))

if __name__ == '__main__':
    main()