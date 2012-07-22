import os

from distutils.core import setup

images = []

for dirpath, dirnames, filenames in os.walk('images'):
  for f in filenames:
    images.append('images/' + f)

db = []

for dirpath, dirnames, filenames in os.walk('db'):
  db = filenames

log = []

for dirpath, dirnames, filenames in os.walk('log'):
  log = filenames

setup(name="Aplicacion de ejemplo",
      version="0.1",
      description="Ejemplo del funcionamiento de distutils",
      author="Raul Gonzalez",
      author_email="zootropo en gmail",
      url="http://mundogeek.net/tutorial-python/",
      license="GPL",
      scripts=["runLinux.py"],
      packages=["modules"],
      py_modules=["Sofia"],
      data_files=[('db', db), ('images', images), ('log', log)]
)

