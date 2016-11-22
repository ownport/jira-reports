
import importlib

def import_module(name, package=None):
    ''' returns imported module (vendored)
    '''
    package_prefix = ''
    if package and package_exists(package):
        package_prefix = '%s.' % package

    params = (package_prefix, name)
    return importlib.import_module('%svendor.%s' % params)


def package_exists(name):
    ''' check if package exists and can be imported
    '''
    try:
        __import__(name)
    except ImportError:
        return False
    else:
        return True
