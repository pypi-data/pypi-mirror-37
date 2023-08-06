
# import modules
from random import uniform
from time import time
from datetime import datetime


def randdate(num, posix_start=0, posix_end=None):
    # set default
    if posix_end is None:
        posix_end = time()

    # generate random posix timestamps
    return [datetime.fromtimestamp(uniform(
        posix_start, posix_end)) for _ in range(num)]
