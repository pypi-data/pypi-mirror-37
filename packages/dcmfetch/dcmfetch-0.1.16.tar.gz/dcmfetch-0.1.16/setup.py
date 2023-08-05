from __future__ import division, print_function, absolute_import
from setuptools import setup
from os.path import join, dirname
import sys
import unittest

# single version
__version__ = 'UNDEFINED'
# version.py should contain just the one line: __version__ == 'X.Y.Z'
with open(join(dirname(__file__), 'dcmfetch', 'version.py')) as f:
    exec(f.read())


def readme(fname):
    path = join(dirname(__file__), fname)
    try:
        import pypandoc
        return pypandoc.convert(path, 'rst')
    except ImportError:
        with open(path) as f:
            return f.read()


def test_suite():
    print('testsuite called')
    return unittest.TestLoader().discover('tests', pattern='test_*.py')


dependencies = ['requests>=2.2.1', 'QtPy>=1.0.2', 'pydicom>=0.9.9']
if sys.version_info < (2, 7):
    dependencies.append('ordereddict')

setup(
    name='dcmfetch',
    version=__version__,
    description='DICOM query retrieve tools',
    long_description=readme('README.md'),
    author='Ron Hartley-Davies',
    author_email='R.Hartley-Davies@bristol.ac.uk',
    url='https://bitbucket.org/rtrhd/dcmfetch',
    download_url='https://bitbucket.org/rtrhd/dcmfetch/get/v%s.zip' % __version__,
    license='MIT',
    install_requires=dependencies,
    tests_require=['pydicom'],
    test_suite="setup.test_suite",
    packages=['dcmfetch'],
    entry_points={
        'console_scripts': ['dcmfetch = dcmfetch.dcmfetch:main'],
        'gui_scripts': ['dcmfetchtool = dcmfetch.dcmfetchtool:main']
    },
    package_data={'dcmfetch': ['ext/findscu*', 'ext/getscu*', 'ext/dcmnodes.cf', 'ext/store-tcs.properties']},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ]
)
