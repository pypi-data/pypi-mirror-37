import os
from setuptools import setup, find_packages


REQUIREMENTS_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'requirements.txt')
)


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith('#')]


setup(
    name='arachno',
    version='0.2.0',
    url='https://github.com/palestamp/arachno',
    author='Stas Kazhavets',
    author_email='stas.kozhevets@gmail.com',
    description='DSL for coroutine orchestration',
    packages=find_packages(exclude=['tests']),
    install_requires=parse_requirements(REQUIREMENTS_PATH),
    long_description=open('README.rst').read(),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
