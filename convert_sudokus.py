#credits to Sander

def create_files():
    # Open the file with 1000 sudokus and create separate files in DIMAC format (clauses)
    with open('1000 sudokus.txt', 'rU') as f:
        k = 0
        for filecount, line in enumerate(f):
            file = []
            for i, row in enumerate(range(1, 10)):
                for j, col in enumerate(range(1, 10)):
                    pos = int(str('{}'.format(row) + '{}'.format(col)))
                    tot = (i * 9) + j

                    if line[tot] != '.':
                        val = int((str(pos) + str(line[tot])))
                        file.append(val)
            k += 1
            if k < 10:
                f = open(("%i sudo.txt" % k) .format(filecount), "w+")
                for value in file:
                    f.write('{} 0\n'.format(value))

create_files()