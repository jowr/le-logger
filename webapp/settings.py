import os
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
        self.__dict__[name] = value 

const = _const()
const.BASE_PATH = os.path.realpath(os.path.dirname(__file__))
const.TEMP_PATH = os.path.join(const.BASE_PATH,'templates')
const.STAT_PATH = os.path.join(const.BASE_PATH,'static')
const.DATA_PATH = os.path.join(const.BASE_PATH,'data')

if 'DYNO' in os.environ:
    const.HEROKU = True
else:
    const.HEROKU = False

if const.HEROKU:
    urlparse.uses_netloc.append("postgres")
    const.PGDB_URI = os.environ["DATABASE_URL"] # postgres://{user}:{password}@{hostname}:{port}/{database-name}
    url = urlparse.urlparse(const.PGDB_URI)
    const.PGDB_NAME = url.path[1:]
    const.PGDB_USER = url.username
    const.PGDB_PASS = url.password
    const.PGDB_HOST = url.hostname
    const.PGDB_PORT = url.port
else:
    from private import PGDB_NAME, PGDB_USER, PGDB_PASS, PGDB_HOST, PGDB_PORT, PGDB_URI
    const.PGDB_URI = PGDB_URI
    const.PGDB_NAME = PGDB_NAME
    const.PGDB_USER = PGDB_USER
    const.PGDB_PASS = PGDB_PASS
    const.PGDB_HOST = PGDB_HOST
    const.PGDB_PORT = PGDB_PORT
