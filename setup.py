from setuptools import setup, find_packages

setup(
    name='foal',
    version='0.1.0',
    license='MIT',
    description='Foundations of Algorithms with Python3',
    long_description=open('README.md', 'r').read(),

    author='Wei Ma',
    author_email='Wei-Ma@outlook.com.au',
    url='https://github.com/Robert-Ma/foal',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[],
)
