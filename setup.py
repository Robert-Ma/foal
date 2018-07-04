from setuptools import setup, find_packages

setup(
    name='eagle',
    version='0.1.0',
    license='MIT',
    description='Basic Algorithms with Python',

    author='Wei Ma',
    author_email='Wei-Ma@outlook.com.au',
    url=None,

    packges=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[],
)
