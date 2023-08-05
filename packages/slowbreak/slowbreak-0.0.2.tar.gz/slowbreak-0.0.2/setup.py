import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()
    
about = {}
with open(os.path.join('slowbreak', '__version__.py'), 'r') as f:
    exec(f.read(), about)

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=about['__url__'],
    packages=setuptools.find_packages(exclude=('*.test',)),
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Financial and Insurance Industry"
    ),
    install_requires=[
        'six'
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
)