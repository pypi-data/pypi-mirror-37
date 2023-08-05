# -*- coding: utf-8 -*-
import sys
from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


if sys.version_info[0] == 2:
    install_requires = [
        'suds',
    ]
else:
    install_requires = [
        'suds-py3',
    ]


setup(
    name='easywsy',
    version='4.0.1',
    description='Simple Web Service development API based on suds',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.e-mips.com.ar/infra/easywsy',
    author='Martín Nicolás Cuesta',
    author_email='cuesta.martin.n@hotmail.com',
    maintainer="Eynes & E-MIPS",
    maintainer_email="cuesta.martin.n@hotmail.com",
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],

    packages=['easywsy', 'easywsy.api', 'easywsy.ws',
              'easywsy.error', 'easywsy.check'],
    license='AGPL3+',
    install_requires=install_requires,
    zip_safe=False,
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
