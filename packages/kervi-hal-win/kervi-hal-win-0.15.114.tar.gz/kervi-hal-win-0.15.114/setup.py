import distutils
from setuptools import setup

import sys

VERSION = "0.0.0"
if '--version' in sys.argv:
    index = sys.argv.index('--version')
    sys.argv.pop(index)
    VERSION = sys.argv.pop(index)


try:
    distutils.dir_util.remove_tree("dist")
except:
    pass

setup(
    name='kervi-hal-win',
    version=VERSION,
    packages=[
        "kervi/platforms/windows",
    ],
    install_requires=[
        'psutil',
        'inputs'
    ],

)