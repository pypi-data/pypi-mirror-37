import sys
import webbrowser
from distutils.core import setup

# Code inspired by Pytorch's pypi source.

trailer_url = 'https://github.com/Microsoft/TextWorld'
message = ("You should install textworld by git cloning"
           " https://github.com/Microsoft/TextWorld and"
           " running `pip install .` instead.")

argv = lambda x: x in sys.argv

if (argv('install') or  # pip install ..
        (argv('--dist-dir') and argv('bdist_egg'))):  # easy_install
    webbrowser.open_new(trailer_url)
    raise Exception(message)


if argv('bdist_wheel'):  # modern pip install
    raise Exception(message)


setup(
    name='textworld',
    version='0.0.3',
    maintainer='Marc-Alexandre Côté',
    maintainer_email='textworld@microsoft.com',
    long_description=message,
    url=trailer_url,
)
