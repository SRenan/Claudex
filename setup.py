"""
Setup script for AOE2 Record APM Analyzer
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="aoe2-apm-analyzer",
    version="1.0.0",
    author="AOE2 APM Tool Contributors",
    description="Extract player APM from Age of Empires 2 recorded game files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/aoe2-apm-analyzer",
    py_modules=['apm_analyzer', 'apm_cli'],
    install_requires=[
        'mgz>=1.8.0',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'aoe2-apm=apm_cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Real Time Strategy",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="aoe2 age-of-empires gaming statistics apm",
)
