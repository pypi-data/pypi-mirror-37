from setuptools import setup
from datareducer.__init__ import __version__ as version, __name__ as name
import sys

SETUP_VARS = dict(
  name=name,
  version=version,
  url='https://github.com/vnl2k/datareducer',
  packages=['datareducer'],
  install_requires=['numpy>=1.14.0', "funkpy>=1.0.1"],
  extras_require={
    'Cython':  ["Cython>=0.28.3"]
  },
  author="vnl2k",
  license='MIT',
  python_requires='>=3.5'
)

try:
  from setuptools.extension import Extension
  from Cython.Build import cythonize

  # It is triggered only when building the installation package:
  #    python3 setup.py sdist
  # Otherwise, cythonize does NOT build the .c files from .pyx
  if "sdist" in sys.argv:
    cythonize("./datareducer/utils.pyx")


  extensions = [
    Extension(
      "datareducer.utils", 
      ["datareducer/utils.c"]
    )
  ]

  SETUP_VARS.update({"zip_safe": False})
  SETUP_VARS.update({"ext_modules": cythonize(extensions)})

  setup(**SETUP_VARS)

except ImportError as e:
  setup(**SETUP_VARS)
