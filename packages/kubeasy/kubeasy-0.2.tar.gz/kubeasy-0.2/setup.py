import os
from setuptools import setup, find_packages

setup(
    name='kubeasy',
    version='0.2',
    py_modules=['kubeasy'],
    author='Cizer Pereira',
    author_email='cizer.ciz@gmail.com',
    url='https://github.com/C123R/kubeasy',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'colorama',
        'PyYAML',
        'PTable',
        'pylint',
        'kubernetes'
    ],
    entry_points='''
        [console_scripts]
        kubeasy=kubeasy:cli
    ''',
)

