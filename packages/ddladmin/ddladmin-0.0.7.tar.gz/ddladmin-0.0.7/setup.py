import setuptools

version_keyword = "Version"
version = "0.0.7"
with open("README.md", "r") as fh:
    long_description = fh.read()

    print("Version: {}".format(version))
    setuptools.setup(
        name="ddladmin",
        version=version,
        author="Shen Wang",
        author_email = 'nedlitex0053@gmail.com',
        description="cli for distributed deep learning admin portal",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages(),
        entry_points={
            'console_scripts': [
                'ddladmin=admincli.cli:main',
            ],
        },
        install_requires=[
            'requests'
        ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )