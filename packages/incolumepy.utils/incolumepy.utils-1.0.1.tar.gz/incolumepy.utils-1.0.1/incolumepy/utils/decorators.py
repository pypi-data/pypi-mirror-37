from time import time
from functools import wraps


def time_it(func):
    '''
    Retorne a string with execution time
    :param func: instance of Function
    :return: string in miliseconds
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print('{}: {:3.5f} ms'.format(func.__name__, 1000 * (end - start)))
        return result
    return wrapper
