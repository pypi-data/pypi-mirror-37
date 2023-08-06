import io
from os.path import dirname, join
from setuptools import setup

def get_version(relpath):
  '''Read version info from a file without importing it'''
  for line in io.open(join(dirname(__file__), relpath), encoding='cp437'):
    if '__version__' in line:
      if '"' in line:
        # __version__ = "0.9"
        return line.split('"')[1]
      elif "'" in line:
        return line.split("'")[1]

setup(
    name='fluas',
    version=get_version("fluas/__init__.py"),
    url='',
    license='',
    author='Joe Brown',
    author_email='joe.brown@pnnl.gov',
    description='',
    long_description='',
    packages=['fluas'],
    install_requires=[
        'matplotlib',
        'pandas',
        'pysam',
        'sarge',
        'seaborn',
    ],
    entry_points={
          'console_scripts': [
              'fluas = fluas.__main__:main'
          ]
    },
)
