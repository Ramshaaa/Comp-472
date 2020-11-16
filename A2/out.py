def solutionFile(data, fileName):
    with open(fileName + '.txt', 'w') as f:
        if data is None:
            f.write('no solution')
        else:
            for x in data[0]:
                out = ''
                for y in x:

                    if type(y) is list:
                        for w in y:
                            out += str(w) + ' '
                    else:
                        out += str(y) + ' '
                f.write(out + '\n')
            f.write(f'{data[1]} %6.3f ' % data[2])


def searchFile(data, fileName):
    with open(fileName + '.txt', 'w') as f:
        if data is None:
            f.write('no solution')
        else:
            for x in data:
                out = ''
                for y in x:
                    if type(y) is list:
                        for w in y:
                            out += str(w) + ' '
                    else:
                        out += str(y) + ' '
                f.write(out + '\n')
