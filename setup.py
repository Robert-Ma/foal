from setuptools import setup, find_packages

setup(
    name='foal',
    version='0.1.0',
    license='MIT',
    description='Foundations of Algorithms with Python3',

    author='Wei Ma',
    author_email='Wei-Ma@outlook.com.au',
    url=None,

    packges=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[],
)
