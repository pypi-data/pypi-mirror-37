from setuptools import setup, find_packages

import gfa_logging

setup(

    name='gfa_logging',

    version=gfa_logging.__version__,

    packages=find_packages(),

    author="Christophe Bastin",

    description="This library provide a logging class to record data or debug your application",

    long_description=open('README.rst').read(),

    # install_requires= ,

    # Use MANIFEST.in
    include_package_data=True,

    url='http://github.com/UMONS-GFA/gfa_logging',

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
    ],

    license="GPL3",
)
