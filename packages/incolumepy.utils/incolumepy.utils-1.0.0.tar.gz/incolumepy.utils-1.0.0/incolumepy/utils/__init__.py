from functools import wraps
from os.path import abspath, join, dirname
from incolumepy.utils.utils import namespace, read

# __version__ = open(abspath(join(dirname(__file__), 'version.txt'))).read().strip()
__version__ = read('version.txt')
__title__ = 'incolumepy.utils'
__namespace__ = namespace(__title__)
__name__ = __title__.split('.')[-1]

def nonexequi(a_func):
    ''' This decorator when apply over def, the def dont work, but return a message informing that skip.

    :param a_func: any function
    :return: str = "Skip: a_function_name"
    '''
    @wraps(a_func)
    def wrap_the_function(self):
        return 'Skip: {}'.format(a_func.__name__)

    return wrap_the_function

