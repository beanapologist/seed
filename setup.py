"""
GoldenSeed Package Setup

Deterministic high-entropy byte stream generation library for procedural content generation,
reproducible testing, and space-efficient storage. NOT FOR CRYPTOGRAPHIC USE.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="golden-seed",
    version="3.0.0",
    description="GoldenSeed — Infinite reproducible high-entropy streams from tiny fixed seeds. For procedural generation, reproducible testing, and deterministic simulations. NOT FOR CRYPTOGRAPHY.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="beanapologist",
    url="https://github.com/beanapologist/seed",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[],  # Zero dependencies for maximum portability
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "gq-universal=gq.cli.universal:main",
            "gq-test-vectors=gq.cli.gqs1:main",
            "gq-coin-flip=gq.cli.golden_ratio_coin_flip:main",
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Games/Entertainment",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    keywords=" ".join([
        "procedural-generation",
        "deterministic",
        "prng",
        "reproducible-testing",
        "pseudo-random",
        "deterministic-streams",
        "consensus",
        "golden-ratio",
        "procedural-content",
        "space-efficient-storage",
        "game-development",
        "simulation",
        "testing",
        "data-compression",
        "deterministic-algorithms",
        "data-teleportation",
        "extreme-compression",
        "public-good-software",
        "seed-generation",
        "binary-watermarking",
        "data-reconstruction",
    ]),
    project_urls={
        "Bug Reports": "https://github.com/beanapologist/seed/issues",
        "Source": "https://github.com/beanapologist/seed",
        "Documentation": "https://github.com/beanapologist/seed#readme",
    },
)
