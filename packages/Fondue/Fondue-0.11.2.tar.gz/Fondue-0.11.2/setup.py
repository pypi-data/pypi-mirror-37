from setuptools import setup
from setuptools.extension import Extension


from fondue import __version__

with open('README.rst', 'r') as f:
    long_description = f.read()

USE_CYTHON = False
ext = '.pyx' if USE_CYTHON else '.c'
extensions = [Extension('fondue.protocol', ['fondue/protocol%s' % ext]),
              Extension('fondue.parser', ['fondue/parser%s' % ext])]

if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions, compiler_directives={'language_level': 3, 'boundscheck': True}, gdb_debug=True,
                           annotate=True)

setup(name='Fondue',
      version=__version__,
      description='Connect peers on a virtual LAN, punching through network barriers.',
      long_description=long_description,
      author='Ariel Antonitis',
      author_email='arant@mit.edu',
      #url='https://github.com/arantonitis/fondue', TODO
      packages=['fondue'],
      package_data={'fondue': '.pyx'},
      ext_modules=extensions,
      entry_points={'console_scripts': ['fondue = fondue.__main__:main']},
      license='MIT',
      classifiers=['License :: OSI Approved :: MIT License',
                   'Development Status :: 2 - Pre-Alpha',
                   'Topic :: System :: Networking',
                   'Topic :: Internet'],
      install_requires=['uvloop'],
      python_requires='>=3.5',
      )
