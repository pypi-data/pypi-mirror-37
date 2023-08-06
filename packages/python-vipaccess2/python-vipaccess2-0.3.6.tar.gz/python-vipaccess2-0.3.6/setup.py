from setuptools import setup
from io import open

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='python-vipaccess2',
    version='0.3.6',
    description="A free software implementation of Symantec's VIP Access application and protocol, a fork of a fork.",
    long_description=readme,
    url='https://github.com/chris17453/python-vipaccess',
    author='Forest Crossman',
    author_email='cyrozap@gmail.com',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='development',
    packages=['vipaccess2'],
    install_requires=[
        'lxml==4.2.5',
        'oath>=1.4.1',
        'pycryptodome==3.6.6',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'vipaccess2=vipaccess2.cli:main',
        ],
    },
    test_suite='nose.collector',
)
