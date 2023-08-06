#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 et:

from os.path import join, dirname
from setuptools import setup, find_packages
import ssc32

def desc():
    return open(join(dirname(__file__), 'README.rst')).read() \
            + '\n' \
            + open(join(dirname(__file__), 'ChangeLog.rst')).read()

setup(
    name="pyssc32",
    description="""SSC32 controlling library""",
    long_description=desc(),
    license="MIT",
    version = ssc32.__version__,
    author = ssc32.__author__,
    author_email = ssc32.__email__,
    url = "https://bitbucket.org/vooon/pyssc32/",
    download_url = 'https://bitbucket.org/vooon/pyssc32/get/%s.tar.gz' % ssc32.__version__,
    keywords = ['SSC32', 'Robotics', 'library'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],
    packages = ['ssc32'],
    scripts = ['ssc32yaml.py'],
    install_requires = ['pyserial', 'pyyaml'],
    platforms = 'any',
)
