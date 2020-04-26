from os import path

from setuptools import setup

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

requirements = [
    'aiohttp',
    'autobahn',
    'cbor'
]

dev_requirements = [
    'pytest',
    'pytest-pep8'
]

setup(
    name='demo-data',
    version='0.0.1',
    packages=['my_reader'],
    url='',
    license='',
    author='prakash',
    author_email='',
    description='',
    long_description=long_description,
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements
    },
    python_requires='>=3.8',
    entry_points={
        "console_scripts": [
            "demo-data = my_reader.house_price:exec_app",
        ]
    }
)