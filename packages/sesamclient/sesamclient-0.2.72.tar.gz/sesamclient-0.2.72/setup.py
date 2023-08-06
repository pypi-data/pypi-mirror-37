# Copyright (C) Bouvet ASA - All Rights Reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
import os

from setuptools import setup, find_packages

requires = [
    "appdirs>=1.4.3",
    "ijson>=2.3",
    "python-dateutil>=2.5.3",
    "pyyaml>=3.12",
    "requests>=2.18.4",
    "PyInstaller>=3.2",
    "nose>=1.3.7",
    "cryptography>=2.1.4",
    "PyJWT>=1.4.1",
]

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()

with open(os.path.join(here, "sesamclient", 'VERSION.txt')) as f:
    VERSION = f.read().strip()

setup(name='sesamclient',
      version=VERSION,
      description='sesamapi client',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP",
      ],
      author='Sesam',
      url='http://sesam.io',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      setup_requires=['pip'],
      test_suite="nose.collector",
      install_requires=requires,
      entry_points={
          'console_scripts': [
               'sesam=sesamclient.main.main:main',
          ],
      })
