from setuptools import setup, find_packages

setup(
    name='amberai-ice-rpc',
    version='1.0.1',
    description='AMBER AI group dedicated RPC framwork call sdk base rp',
    author='chn1807',
    author_email='chn1807@163.com',
    maintainer='chn1807',
    maintainer_email='chn1807@163.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'zeroc-ice==3.7.1'
    ],
    keywords='amberai ice rpc'
)