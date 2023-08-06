import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="riscv-model",
    version="0.0.1",
    author="Stefan Wallentowitz",
    author_email="stefan@wallentowitz.de",
    description="RISC-V Model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wallento/riscv-python-model",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)