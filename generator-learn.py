def makegenerator(src):
    with open(src) as f:
        for str in f:
            yield str



if __name__ == '__main__':
    c = makegenerator('dest.txt')
    for x in c:
        print x