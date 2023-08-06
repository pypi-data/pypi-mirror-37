import os


def safe_open(filename, mode='rb'):

    if not os.path.isfile(filename):
        print 'file not exists: {}'.format(filename)
        exit(1)

    return open(filename, mode)
