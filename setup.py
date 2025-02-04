from setuptools import setup, find_packages

setup(
    name="PDF417_Scanner",
    version="0.2",
    author="Yash",
    description="this is the version 0.2 that has flask api and front end for image scanning, video scanning and returning the data",
    url="https://github.com/T-Yashwanth/PDF417-Scanner",
    packages=find_packages(),
    package_dir={"": "src"},
)