import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="j_builds",
    version="0.0.2",
    author="Acciaioli Valverde",
    author_email="acci.valverde@gmail.com",
    description="Build and Deploy!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Spin14/j-builder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
    scripts=['bin/j-build'],
    install_requires=['termcolor'],
)    
