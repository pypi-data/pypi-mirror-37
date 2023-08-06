
from setuptools import setup

with open('requirements.txt') as f:
    install_packs = f.read().splitlines()
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pycrypt-samn',
    version='1.2.1',
    description='Customized Encryption module',
    license='Apache',
    packages=['pycrypt'],
    install_requires=install_packs,
    author='Sammy Shuck github.com/ToxicSamN',
    keywords=['pycrypt', 'pycrypt-samn'],
    url='https://github.com/ToxicSamN/pycrypt'
)
