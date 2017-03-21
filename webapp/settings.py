import os
import psycopg2
import urlparse

# from http://code.activestate.com/recipes/65207-constants-in-python
class _const:
    class ConstError(TypeError): pass  # base exception class
    class ConstCaseError(ConstError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const.%s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name %r is not all uppercase' % name)
        self.__dict__[name]

const = _const()
const.BASE_PATH = os.path.realpath(os.path.dirname(__file__))
const.TEMP_PATH = os.path.join(BASE_PATH,'templates')

if 'DYNO' in os.environ:
    const.HEROKU = True
else:
    const.HEROKU = False