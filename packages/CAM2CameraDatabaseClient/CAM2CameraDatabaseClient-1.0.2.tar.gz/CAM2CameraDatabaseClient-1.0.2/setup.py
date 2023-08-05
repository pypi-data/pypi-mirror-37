from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'CAM2CameraDatabaseClient',
    packages = find_packages(exclude = ['contrib', 'docs', 'tests']),
    version = '1.0.2',
    description = 'A python wrapper of CAM2 database API',
    long_description = long_description,
    long_description_content_type='text/markdown',
    author = 'Purdue CAM2 Research Group',
    author_email = 'cam2proj@ecn.purdue.edu',
    #license='Apache License 2.0',
    url = 'https://github.com/PurdueCAM2Project/CameraDatabaseClient',
    keywords = ['API','camera', 'database', 'CAM2'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        #'License :: OSI Approved :: Apache Software License'
    ],
    python_requires = '>=2.7',
    install_requires = ['requests']
)
