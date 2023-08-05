# ===============================================================================
# Copyright 2017 dgketchum
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

import os

from setuptools import setup

os.environ['TRAVIS_CI'] = 'True'

try:
    from setuptools import setup

    setup_kwargs = {}
except ImportError:
    from distutils.core import setup

    setup_kwargs = {}

with open('README.md') as f:
    readme = f.read()

tag = '0.0.5'

setup(name='bounds',
      version=tag,
      description='Very simple API return geographic or projected coordinates from raster or '
                  'iterable',
      long_description=readme,
      setup_requires=['nose>=1.0'],
      py_modules=['bounds'],
      license='Apache',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: GIS',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6'],
      keywords='raster analysis',
      author='David Ketchum',
      author_email='dgketchum@gmail.com',
      platforms='Posix; MacOS X; Windows',
      packages=[],
      download_url='https://github.com/{}/{}/archive/{}.tar.gz'.format('dgketchum', 'bounds', tag),
      url='https://github.com/dgketchum/bounds',
      test_suite='',
      install_requires=['rasterio', 'pyproj'],
      **setup_kwargs)


# ============= EOF ==============================================================
