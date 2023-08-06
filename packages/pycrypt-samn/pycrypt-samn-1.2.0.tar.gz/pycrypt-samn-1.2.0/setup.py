
from setuptools import setup

with open('requirements.txt') as f:
    install_packs = f.read().splitlines()


setup(
    name='pycrypt-samn',
    version='1.2.0',
    description='Customized Encryption module',
    license='Apache',
    packages=['pycrypt'],
    install_requires=install_packs,
    author='Sammy Shuck github.com/ToxicSamN',
    keywords=['pycrypt', 'pycrypt-samn'],
    url='https://github.com/ToxicSamN/pycrypt'
)
