from setuptools import setup, find_packages
from os import path
import sys
here = path.abspath(path.dirname(__file__))


if sys.version_info[0]>2:
  with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
else:    
  with open(path.join(here, 'README.rst')) as f:  
    long_description = f.read().decode("UTF-8")

setup_defaults = {  
   'name'        : 'fc_oogmsh',
   'description' : 'Generate and read mesh files by using gmsh and given .geo files',
   'version'     : '0.0.6',
   'url'         : 'http://www.math.univ-paris13.fr/~cuvelier/software',
   'author'      : 'Francois Cuvelier',
   'author_email': 'cuvelier@math.univ-paris13.fr',
   'license'     : 'BSD',
   'packages'    : ['fc_oogmsh'],
   'classifiers':['Topic :: Scientific/Engineering'],
   } 

setup(name=setup_defaults['name'],
      description = setup_defaults['description'],
      long_description=long_description,
      version=setup_defaults['version'],
      url=setup_defaults['url'],
      author=setup_defaults['author'],
      author_email=setup_defaults['author_email'],
      license = setup_defaults['license'],
      platforms=["Linux"],#, "Mac OS-X", 'Windows'],
      #packages=setup_defaults['packages'],
      packages=find_packages('src'),  # include all packages under src
      package_dir={'':'src'},   # tell distutils packages are under src
      classifiers=setup_defaults['classifiers'],
      install_requires=['fc_tools >= 0.0.20','appdirs'],
      package_data={
        'fc_oogmsh': ['geodir/2d/*.geo','geodir/3d/*.geo','geodir/3ds/*.geo'],
      }
     )
