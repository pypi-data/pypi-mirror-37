import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="playoff_core",
    version="0.8.3",
    author="Mattia Bano",
    author_email="dev@officina.cc",
    description="Playoff toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/officina/playoff-core",
    packages=setuptools.find_packages(),
    install_requires=[
        "Playoff",
        "jwt",
        "python-dotenv"

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
