# HRV SETUP SCRIPT

import setuptools
from pyhrv import __author__, __version__, __email__, name, description

with open("README.md", "r") as fh:
	long_description = fh.read()

# Required Python distribution
REQUIRES_PYTHON = '>=2.7.10'

# Required packages in order for this package to work
REQUIRED = [
	'biosppy',
	'matplotlib',
	'numpy',
	'scipy',
	'nolds'
]

# Create setup
setuptools.setup(
	name=name,
	version=__version__,
	author=__author__,
	author_email=__email__,
	description=description,
	long_description=long_description,
	long_description_content_type="text/markdown",
	python_requires=REQUIRES_PYTHON,
	url="https://github.com/PGomes92/pyhrv",
	packages=setuptools.find_packages(),
	install_requires=REQUIRED,
	classifiers=[
		'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'Intended Audience :: Science/Research',
		'Natural Language :: English',
		'License :: OSI Approved :: BSD License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: Implementation :: CPython',
		'Programming Language :: Python :: Implementation :: PyPy',
		'Operating System :: OS Independent',
	],
)
