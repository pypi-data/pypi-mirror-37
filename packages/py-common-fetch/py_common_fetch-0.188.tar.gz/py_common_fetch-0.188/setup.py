from setuptools import setup
from codecs import open
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    author='Greg flores',
    author_email='bygregonline@yahoo.com',
    license='MIT',
    zip_safe=False,
    packages=['aniachi'],
    name='py_common_fetch',    # This is the name of your PyPI-package.
    version='0.188',                          # Update the version number for new releases
    scripts=['aniachi/timeUtils.py', 'aniachi/stringUtils.py','aniachi/systemUtils.py'],   
    keywords='noefetch common information welcome screen',
    install_requires=['pip>=10.0.1', 'psutil>=5.4.5','json2html','py-cpuinfo','termcolor'],
    url='https://github.com/bygregonline/py-common-fetch',
    description='A really simple to use Python fetch screen',
    long_description_content_type='text/markdown',
    long_description=long_description  # Optional

)