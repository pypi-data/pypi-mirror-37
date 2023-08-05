import re
import ast

__author__ = "Cristian Perez"
__copyright__ = "Copyright 2017, Cristian Perez"
__email__ = "Vilero89@gmail.com"
__license__ = "MIT"

try:
    from setuptools import setup, find_packages
except ImportError:
    raise Exception("Please install setuptools.")

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('ibio/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='ibio',
    version=version,
    description='Package with bioinformatical utilities',
    url='https://github.com/crispgc/ibio',
    author='Cristian Perez',
    author_email='Vilero89@gmail.com',
    license='GNU General Public License v3.0',
    packages=find_packages(),
    zip_safe=False,
    python_requires='>=3.6',
    package_data={'': ['*.css', '*.sh', '*.html']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        "console_scripts":
            [
                "ibio=ibio:main",
            ]
    },
    install_requires=[],
)
