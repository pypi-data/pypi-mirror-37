
import setuptools
from setuptools import setup

with open('requirements.txt') as f:
    install_packs = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyucs-samn',
    version='1.2.0',
    description='Customized UCS Python Module',
	long_description=long_description,
    license='Apache',
    packages=setuptools.find_packages(),
    install_requires=install_packs,
    author='Sammy Shuck github.com/ToxicSamN',
    keywords=['pyucs', 'pyucs-samn'],
    url='https://github.com/ToxicSamN/pyucs'
)
