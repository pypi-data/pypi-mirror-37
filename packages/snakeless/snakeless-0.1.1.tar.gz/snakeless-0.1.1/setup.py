import setuptools

PROJECT = "snakeless"

VERSION = "0.1.1"

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name=PROJECT,
    version=VERSION,
    author="German Ivanov",
    author_email="germivanov@gmail.com",
    description="Create Google Cloud based serverless apps with joy",
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/tasyp/snakeless",
    install_requires=[
        "cliff",
        "halo",
        "pyyaml",
        "schema",
        "google-auth",
        "apiron",
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["snakeless = snakeless:main"],
        "snakeless.cli": [
            "check = snakeless.commands:Check",
            "deploy = snakeless.commands:Deploy",
        ],
    },
    zip_safe=False,
)
