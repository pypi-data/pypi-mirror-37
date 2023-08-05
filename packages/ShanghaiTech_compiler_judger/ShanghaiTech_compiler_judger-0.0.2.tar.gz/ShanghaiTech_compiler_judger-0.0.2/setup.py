from setuptools import setup
from setuptools import find_packages
from os.path import join, dirname
# We need io.open() (Python 3's default open) to specify file encodings
import io
import sys

version = '0.0.2'

try:
    # obtain long description from README and CHANGES
    # Specify encoding to get a unicode type in Python 2 and a str in Python 3
    with io.open(
            join(dirname(__file__), 'README.md'),
            'r',
            encoding='utf-8') as f:  # type: ignore
        README = f.read()
except IOError:
    README = ''

install_requires = [
    'requests',
    'setuptools',
    'GitPython',
    'packaging',
    'future',
    'tqdm'
]

tests_require = [
    'pytest',
    'pytest-cov',
]

setup(
    name="ShanghaiTech_compiler_judger",
    version=version,
    description="Tools for ShanghaiTech Compiler course. ",
    long_description=README,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="",
    author="Q7",
    author_email="q71998@gmail.com",
    license="MIT",
    packages=find_packages(),
    scripts=[
        'compiler-test-setup',
        'compiler-test',
        'compiler-submit',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'testing': tests_require,
    },
)
