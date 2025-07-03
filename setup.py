"""
Setup configuration for ElevenLabs Batch Calling Data Processor.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="elevenlabs-batch-processor",
    version="1.0.0",
    author="ieiskyler",
    author_email="your.email@example.com",
    description="A Python toolkit for managing and processing ElevenLabs batch calling data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ieiskyler/elevenlabs-batch-processor",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Telephony",
        "Topic :: Office/Business",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "elevenlabs-batch-history=src.batch_history:main",
            "elevenlabs-batch-converter=src.batch_converter:main",
            "elevenlabs-batch-processor=src.batch_processor:main",
            "elevenlabs-batch-list-converter=src.batch_list_converter:main",
        ],
    },
    keywords="elevenlabs api batch calling data processing csv json",
    project_urls={
        "Bug Reports": "https://github.com/ieiskyler/elevenlabs-batch-processor/issues",
        "Source": "https://github.com/ieiskyler/elevenlabs-batch-processor",
        "Documentation": "https://github.com/ieiskyler/elevenlabs-batch-processor#readme",
    },
)
