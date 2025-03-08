from setuptools import setup, find_packages

setup(
    name="prompt_scaffolding",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "setuptools>=42.0.0",
        "packaging>=20.0",
    ],
    entry_points={
        "console_scripts": [
            "scaffold=src.cli:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A multi-tier pipeline system for generating code projects through progressive LLM prompting",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/prompt-scaffolding",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)