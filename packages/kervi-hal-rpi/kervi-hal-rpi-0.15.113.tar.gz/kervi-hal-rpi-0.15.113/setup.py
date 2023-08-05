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
    name='kervi-hal-rpi',
    version=VERSION,
    description="""Raspberry pi hardware abstraction layer for the Kervi automation framework""",
    packages=[
        "kervi.platforms.raspberry",
        "kervi.devices.raspberry"
    ],
    install_requires=[
        'Adafruit_GPIO',
        'inputs'
    ],

)
