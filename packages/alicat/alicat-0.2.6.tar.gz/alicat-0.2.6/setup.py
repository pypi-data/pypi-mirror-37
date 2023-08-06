"""Install parameters for CLI and python import."""
from setuptools import setup

setup(
    name="alicat",
    version="0.2.6",
    description="Python driver for Alicat mass flow controllers.",
    url="http://github.com/numat/alicat/",
    author="Patrick Fuller",
    author_email="pat@numat-tech.com",
    packages=["alicat"],
    install_requires=["pyserial"],
    entry_points={
        "console_scripts": [("alicat = alicat:command_line")]
    },
    license="GPLv2",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)"
    ]
)
