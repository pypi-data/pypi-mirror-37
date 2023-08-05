from setuptools import setup
setup(
  name = 'CAM2ImageArchiver',
  packages = ['CAM2ImageArchiver'],
  version = '2.0.0',
  description = 'Network camera image retrieval and archiving.',
  author = 'Purdue CAM2 Research Group',
  author_email = 'cam2proj@ecn.purdue.edu',
  license='Apache License 2.0',
  url = 'https://github.com/cam2proj/CAM2ImageArchiver',
  download_url = 'https://github.com/cam2proj/CAM2ImageArchiver/archive/1.0.tar.gz',
  keywords = ['computer', 'vision', 'CAM2'],
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 2.7',
    'License :: OSI Approved :: Apache Software License'
  ],
  python_requires='<3', # Support for V3 has not been fully tested.
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
