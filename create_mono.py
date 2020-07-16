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
            x = str(index + 1)
            monomial = monomial + x
    return monomial

yeet = create_mono([[[0,1,2,1,0], 0], [[0,1,2,1,1], 0], [[0,1,2,1,4],1], [[3,0,0,0,0], 3], [[1,1,1,1,3],4]])
print(yeet)