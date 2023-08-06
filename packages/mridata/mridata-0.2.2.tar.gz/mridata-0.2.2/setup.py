import sys
from setuptools import setup

if sys.version_info < (3, 0):
    sys.exit('Sorry, Python < 3.0 is not supported')

with open("README.md", "r") as f:
    long_description = f.read()
    
setup(name='mridata',
      version='0.2.2',
      description='Python command line interface for downloading and uploading to mridata.org.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/mikgroup/mridata-python',
      author='Frank Ong',
      author_email='frankong@berkeley.edu',
      license='BSD',
      scripts=['bin/mridata'],
      install_requires=[
          'requests',
          'boto3',
          'tqdm'
      ],
      packages=['mridata'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
      ],
)
