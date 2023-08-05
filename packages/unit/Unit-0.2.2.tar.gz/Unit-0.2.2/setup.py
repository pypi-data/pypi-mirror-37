import sys

if sys.version_info < (3, 5):
    raise RuntimeError('Unit requires Python 3.5 or greater')


import pathlib
import setuptools


_ROOT = pathlib.Path(__file__).parent


with open(str(_ROOT / 'README.rst')) as f:
    readme = f.read()


setuptools.setup(
    name='Unit',
    version='0.2.2',
    description='An asynchronous web framework written in Python.',
    long_description=readme,
    url='https://github.com/jiangwwei/unit',
    author='Jiang Wei',
    author_email='jiangweiaz@gmail.com',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
    ],
    packages=['unit'],
    platforms=['POSIX'],
    install_requires=['httptools>=0.0.11'],
    python_requires='>=3.5',
    include_package_data=True,
)
