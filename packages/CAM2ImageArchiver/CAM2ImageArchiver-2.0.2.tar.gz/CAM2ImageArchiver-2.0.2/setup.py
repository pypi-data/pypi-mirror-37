from setuptools import setup
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'CAM2ImageArchiver',
  packages = ['CAM2ImageArchiver'],
  version = '2.0.2',
  description = 'Network camera image retrieval and archiving.',
  long_description = long_description,
  long_description_content_type='text/markdown',
  author = 'Purdue CAM2 Research Group',
  author_email = 'cam2proj@ecn.purdue.edu',
  license='Apache License 2.0',
  url = 'https://github.com/cam2proj/CAM2ImageArchiver',
  download_url = 'https://github.com/cam2proj/CAM2ImageArchiver/archive/1.0.tar.gz',
  keywords = ['computer', 'vision', 'CAM2'],
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: Apache Software License'
  ],
  python_requires='>=2.7',
  install_requires=[
    'certifi',
    'chardet',
    'funcsigs',
    'idna',
    'mock',
    'numpy',
    'pbr',
    'pytz',
    'requests',
    'opencv-python'
  ]
)
