import setuptools

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='egrp365',
    version='0.0.4',
    packages=['egrp365'],
    url='https://github.com/egrp365/python-egrp365-api',
    license='MIT License (MIT)',
    long_description=long_description,
    author='egrp365',
    author_email='mail@egrp365.ru',
    description='This module implements the egrp365.ru HTTP API.',
    install_requires=[
        "requests",
    ],
)
