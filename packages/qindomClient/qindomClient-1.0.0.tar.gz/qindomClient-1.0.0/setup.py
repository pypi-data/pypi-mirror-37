from setuptools import setup, find_packages

setup(
    name="qindomClient",
    version="1.0.0",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2'
    ],
    install_requires=['requests', 'json'],
)
