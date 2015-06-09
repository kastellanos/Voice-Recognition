__author__ = 'Andres'


def load(fname):
    from pickle import load

    with open(fname, 'rb') as file:
        net = load(file)

    return net


def save(net, fname):
    from pickle import dump

    with open(fname, 'wb') as file:
        dump(net, file)