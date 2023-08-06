import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'searchstims'
DESCRIPTION = 'generate images like the stimuli used in visual search experiments'
URL = 'https://github.com/NickleDave/main.py'
EMAIL = 'nicholdav@gmail.com'
AUTHOR = 'David Nicholson'
VERSION = '0.1'
KEYWORDS = ['visual search', 'pygame']

# What packages are required for this module to be executed?
REQUIRED = [
    'pygame',
    'numpy',
]

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    keywords=KEYWORDS,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': ['searchstims=searchstims.main:main'],
    },
    install_requires=REQUIRED,
    python_requires='>=3',
    include_package_data=True,
    license='BSD-3',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: BSD License',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
