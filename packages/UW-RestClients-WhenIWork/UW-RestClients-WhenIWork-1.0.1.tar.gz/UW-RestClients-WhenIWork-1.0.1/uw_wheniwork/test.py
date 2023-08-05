# This is just a test runner for coverage
from os.path import abspath, dirname, join

from commonconf.backends import use_configparser_backend

if __name__ == '__main__':
    path = abspath(join(dirname(__file__), "..", "travis-ci", "test.conf"))
    use_configparser_backend(path, 'WHENIWORK')

    from nose2 import discover
    discover()
