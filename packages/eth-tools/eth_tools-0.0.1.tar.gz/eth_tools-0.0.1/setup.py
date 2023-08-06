from setuptools import setup, find_packages

VERSION = '0.0.1'

setup(
    name='eth_tools',
    version=VERSION,
    license='MIT',
    description='like function listtransactions for bitcoin',
    url='https://github.com/l3n641/eth_tool',
    author='l3n641',
    author_email='hh250@qq.com',
    platforms='any',
    install_requires=[
        'web3',
        'sqlalchemy',

    ],
    packages=find_packages(),
    include_package_data=True,
)
