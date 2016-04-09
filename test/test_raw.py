from os.path import dirname, join

from coinlib.raw import install_raw_package

DIR = dirname(__file__)


def test_install_raw_package():
    install_raw_package(join(DIR, 'cache.dir'), 'test', join(DIR, 'data', 'test.tar.gz'), True, join(DIR, 'install'), 'test')
