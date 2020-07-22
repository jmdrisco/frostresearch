def generate_binary(k):
    binaries = []
    i=0
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


def main():
    k = int(input("Dimension of the input vector: "))
    print(generate_binary(k))


if __name__ == "__main__":
    main()