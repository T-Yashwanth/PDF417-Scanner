from setuptools import setup, find_packages

setup(
    name="PDF417_Scanner",
    version="0.1",
    author="Yash",
    description="This project was created by me from scratch",
    url="https://github.com/T-Yashwanth/PDF417-Scanner",
    packages=find_packages(),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)