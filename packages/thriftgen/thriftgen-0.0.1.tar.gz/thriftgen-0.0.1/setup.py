from setuptools import setup
from setuptools import find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

packages = find_packages()

setup(
    name='thriftgen',
    version='0.0.1',
    description='thriftgen',
    long_description=readme,
    author='Bogdan Mustiata',
    author_email='bogdan.mustiata@gmail.com',
    license='BSD',
    entry_points={
        "console_scripts": [
            "thriftgen = thriftgen.mainapp:main"
        ]
    },
    install_requires=[
        "pybars3 >=0.9.3, <0.10.0",
        "pybars3-extensions >=1.0.0, <1.1.0",
        "antlr4-python3-runtime >=4.7.1, <4.8.0"],
    packages=packages,
    package_data={
        '': ['*.txt', '*.rst']
    })
