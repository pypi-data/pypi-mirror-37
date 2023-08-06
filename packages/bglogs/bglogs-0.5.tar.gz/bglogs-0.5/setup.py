from os import path
from setuptools import setup, find_packages
from bglogs import __version__


directory = path.dirname(path.abspath(__file__))
with open(path.join(directory, 'requirements.txt')) as f:
    required = f.read().splitlines()


setup(
    name='bglogs',
    version=__version__,
    description='BBGLab python logging with customized default formatting and behaviour',
    author="BBGLab",
    author_email="bbglab@irbbarcelona.org",
    url="https://bitbucket.org/bgframework/bglogs/get/{}.tar.gz".format(__version__),
    packages=find_packages(),
    install_requires=required,
    python_requires='>=3.5',
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)