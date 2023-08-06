import codecs
import os
import sys

try:
	from setuptools import setup, find_packages
except:
	from distutils.core import setup

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "SMMSAT",
    version = "0.1.0",
    description = "Soft Matter Molecular Simulation Analysis Toolkit.",
    long_description = read("README.txt"),
    classifiers =
	[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
		'Topic :: Scientific/Engineering :: Astronomy',
		'Topic :: Scientific/Engineering :: GIS',
		'Topic :: Scientific/Engineering :: Mathematics',
		'Intended Audience :: Science/Research',
		'Intended Audience :: Developers',
		'Intended Audience :: Information Technology',
    ],
    install_requires=
	[
        'numpy',
        'pandas',
        'pathlib',
    ],
    keywords = "Soft Matter Molecular Simulation Analysis Toolkit",
    author = "Zhenghao Wu",
    author_email = "w415146142@gmail.com",
    url ="https://github.com/Chenghao-Wu/SMMSAT",
    license = "MIT",
    packages = find_packages(),
    include_package_data= True,
    zip_safe= True,
)