"""
valis
"""
from setuptools import setup, find_packages

DOCLINES = __doc__.split("\n")

setup(
    name='valis',
    author='Salik Syed',
    description=DOCLINES[0],
    long_description="\n".join(DOCLINES[2:]),
    version=0.1,
    packages=find_packages(),
    url='https://github.com/VALIS-software/valis-python-client',
    install_requires=[
        'requests'
    ]
)