import os
try:
    from setuptools import setup, find_packages, Command
except ImportError:
    from distutils.core import setup, Command

BASE_DIR = os.path.dirname(__file__)
README_PATH = os.path.join(BASE_DIR, 'README.md')
DESCRIPTION = open(README_PATH).read()
KEYWORDS = 'Python Flask Server-Timing Header Extension'

setup(
    name='flask-server-timing',
    version='0.1.1',
    description=KEYWORDS,
    long_description=DESCRIPTION,
    license='Apache License 2.0',
    author='Robin Peters',
    author_email='github@rpeters.dk',
    packages=find_packages(),
    install_requires=[
        'Flask>=0.10.1'
    ],
    keywords=KEYWORDS,
    url='https://github.com/rodrobin/flask-server-timing',
    namespace_packages=[],
    platforms='Linux, POSIX',
    entry_points={
        'console_scripts': [
            '',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
