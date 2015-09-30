
from distutils.core import setup, Extension

localtime_module = Extension('_localtime',
                             sources=['localtime.c'])

setup(name="localtime",
      version="2.0.79",
      description="sMAP standard library and drivers",
      author="Stephen Dawson-Haggerty",
      author_email="stevedh@eecs.berkeley.edu",
      url="http://cs.berkeley.edu/~stevedh/smap2/",
      packages=['localtime'],
      ext_modules=[localtime_module])
