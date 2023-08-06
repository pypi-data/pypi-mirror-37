from setuptools import setup


setup(
    name="azblob",
    version="0.0.5",
    author="Philipp Lang",
    packages=["azblob"],
    url=("https://github.com/plang85/azblob"),
    license="MIT License",
    description="Download Azure blobs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development",
    ],
    entry_points={"console_scripts": ["azblob = azblob.ops:cli"]},
    install_requires=[
        "azure-storage-blob>=1.3.0",
        "azure-storage-file>=1.3.0",
        "tqdm>=4.0.0",
        "tabulate>=0.8.2",
    ],
    extras_require={"dev": ["black", "twine"]},
)
