#!/usr/bin/env python

from setuptools import setup


# Modified from http://stackoverflow.com/questions/2058802/
# how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package
def version():
    import os
    import re

    init = os.path.join('sausage_machine', '__init__.py')
    with open(init) as fp:
        initData = fp.read()
    match = re.search(r"^__version__ = ['\"]([^'\"]+)['\"]",
                      initData, re.M)
    if match:
        return match.group(1)
    else:
        raise RuntimeError('Unable to find version string in %r.' % init)


setup(name='sausage-machine',
      version=version(),
      packages=['sausage_machine'],
      include_package_data=True,
      url='https://github.com/VirologyCharite/sausage-machine',
      download_url='https://github.com/VirologyCharite/sausage-machine',
      author='Terry Jones',
      author_email='tcj25@cam.ac.uk',
      keywords=['pipeline'],
      scripts=[
          'bin/sausage-machine-version.py',
      ],
      classifiers=[
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      license='MIT',
      install_requires=[
          'six>=1.10.0',
      ],
      description='A Python class for running / scheduling pipeline jobs')
