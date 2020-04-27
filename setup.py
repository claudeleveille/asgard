import setuptools
from asgard._version import __version__

setuptools.setup(
    name="asgard",
    version=__version__,
    description="ASGARD: SemVer Generator and Release Dispatcher",
    long_description=open("README.md").read(),
    long_description_type="text/markdown",
    author="Claude Léveillé",
    url="https://github.com/claudeleveille/asgard",
    packages=setuptools.find_packages(),
    scripts=["bin/asgard"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Version Control",
        "Topic :: Utilities",
    ],
)
