import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="megapy",
    version="0.0.7",
    author="Aakash Sahai",
    author_email="sahaiaakash@gmail.com",
    description=" A Python package to control Arduino Mega over USB Serial",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aakash-sahai/megapy",
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pyserial>=3.0']
)
