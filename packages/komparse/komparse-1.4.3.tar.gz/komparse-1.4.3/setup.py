from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='komparse',
    version='1.4.3',
    description='A parser combinator library',
    long_description="""
    Komparse is a tiny Python library to build a parser combinator.
    """,
    #url='', TODO: create website for komparse
    author='Thomas Bollmeier',
    author_email='entwickler@tbollmeier.de',
    license='Apache-2.0',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3'
    ],
    keywords='parser development',
    scripts=[],
    packages=['komparse'],
    package_dir={'komparse': 'src/komparse'}
)
