import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cepclient",
    version="0.1",
    author="Chameleon",
    author_email="users@chameleoncloud.org",
    description="Chameleon Experiment Precis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.chameleoncloud.org/",
    packages=['cepclient'],
    license='LICENSE',
    install_requires=[
        "keystoneauth1",
        "prettytable",
        "requests",
    ],
    scripts=['cepclient/cep'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)