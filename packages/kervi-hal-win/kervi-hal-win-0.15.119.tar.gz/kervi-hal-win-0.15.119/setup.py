import distutils
from setuptools import setup

import sys

from kervi.platforms.windows.version import VERSION


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