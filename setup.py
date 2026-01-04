"""
Golden Quantum (GQ) Package Setup

Production-grade Post-Quantum Secure Key Generation package implementing the Golden Consensus Protocol (GCP-1)
and Golden Standard (GQS-1) for deterministic key generation with verified checksums, aligned with NIST 
Post-Quantum Cryptography (PQC) standards for integration with Kyber, Dilithium, and FrodoKEM.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="golden-quantum",
    version="2.0.0",
    description="Post-Quantum Secure Key Generation - Deterministic Keys with Verified Checksums, aligned with NIST PQC standards (Kyber, Dilithium, FrodoKEM) - GCP-1 & GQS-1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="beanapologist",
    url="https://github.com/beanapologist/seed",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[],  # Zero dependencies for maximum security
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
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    keywords="post-quantum-cryptography pqc nist-pqc kyber dilithium frodokem deterministic-key checksum quantum-resistant cryptography consensus blockchain gcp gqs binary-fusion-tap checksums verified-keys",
    project_urls={
        "Bug Reports": "https://github.com/beanapologist/seed/issues",
        "Source": "https://github.com/beanapologist/seed",
        "Documentation": "https://github.com/beanapologist/seed#readme",
    },
    license="GPL-3.0-or-later",
)
