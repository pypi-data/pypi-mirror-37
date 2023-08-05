import numpy  # <- forces us to install numpy BEFORE drizzlib. Help?

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

# Read the version number from the VERSION file
from os.path import abspath, dirname, join

with open(join(dirname(abspath(__file__)), 'VERSION'), 'r') as version_file:
    version = version_file.read().strip()

# Set up our C extension
optimized_module = Extension(
    'optimized',
    sources=[
        'src/optimized.c',
    ],
    include_dirs=[numpy.get_include()]
)

setup(
    name='drizzlib',
    version=version,
    author='Paradis Deborah',
    author_email='deborah.paradis@irap.omp.eu',
    maintainer='Antoine Goutenoir',
    maintainer_email='antoine.goutenoir@irap.omp.eu',
    url='https://gitlab.irap.omp.eu/CADE/drizzlib',


    license='GPL',
    description="Drizzlib is a drizzling module to convert from HEALPIX to "
                "WCS FITS files.",
    ext_modules=[optimized_module],
    # Redundancy with requirements.txt because ... pip T_T
    install_requires=['numpy>=1.11', 'matplotlib>=2.0', 'astropy>=1.0', 'scipy>=0.18', 'healpy>=1.9', 'reproject>=0.4'],
    requires=['numpy', 'matplotlib', 'astropy', 'scipy', 'healpy', 'reproject'],
    ###
    packages=['drizzlib'],
    package_dir={'drizzlib': 'lib'},
    provides=['drizzlib'],
    scripts=['bin/healpix2wcs']

)
