import os
from setuptools import setup, find_packages

setup(
    name="envtoolkit",
    version="1.0.0",
    author="Nicolas Barrier",
    maintainer="Nicolas Barrier",
    author_email="nicolas.barrier@ird.fr",
    maintainer_email="nicolas.barrier@ird.fr",
    url="https://github.com/barriern/Environmental-toolkit",
    description=("Python package dedicated to the Earth Scientists. It contains a module for the processing of time-series (filtering, anomalies), a module for spatial analysis, a module with color-specific functions, a module for NetCDF processing and a module for spectral analysis"),
    license=None,  
    packages=find_packages(),
    keywords="Lanczos; filtering; Masked Lambert Conformal; colormaps; climatologies; anomalies; maps; netcdf",
    long_description=open('README.md').read(),
    requires=['numpy(>=1.9.2)',
              'netCDF4(>=1.1.9)',
              'matplotlib(>=1.43)',
              're(>=2.2)',
              'basemap(>=1.0)',
              'spectrum',
              'datetime'],
    classifiers = [
                    #"Development Status :: 5 - Production/Stable",
                    "Development Status :: 4 - Beta",
                    "Intended Audience :: Science/Research",
                    "Topic :: Scientific/Engineering :: Mathematics",
                    "Topic :: Scientific/Engineering :: Physics",
                    "Topic :: Scientific/Engineering :: Visualization",
                    "Topic :: Scientific/Engineering :: Physics",
                    "License :: Free To Use But Restricted",
                    "Operating System :: MacOS :: MacOS X",
                    "Operating System :: Unix",
                    "Operating System :: POSIX :: Linux",
                    "Programming Language :: Python :: 2.7",
                    ],

    # ++ test_suite =
    # ++ download_url
    platforms=['linux', 'mac osx'],
    )

           
