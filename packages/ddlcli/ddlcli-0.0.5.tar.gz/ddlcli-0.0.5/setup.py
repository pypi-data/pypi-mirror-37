import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ddlcli",
    version="0.0.5",
    author="Yi Lu",
    description="cli for distributed deep learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'ddlcli=ddlcli.cli:main',
        ],
    },
    install_requires=[
        'pyyaml',
        'boto3',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)