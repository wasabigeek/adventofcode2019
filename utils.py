def read_intcode(path):
    "returns array of Integers"
    with open(path) as f:
        intcode = [int(i) for i in f.read().split('\n')[0].split(',')]

    return intcode

