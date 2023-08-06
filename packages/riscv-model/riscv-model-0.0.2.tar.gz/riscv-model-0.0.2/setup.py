import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="riscv-model",
    version="0.0.2",
    author="Stefan Wallentowitz",
    author_email="stefan@wallentowitz.de",
    description="RISC-V Model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wallento/riscv-python-model",
    packages=setuptools.find_packages(),
    entry_points={
      'console_scripts': [
         'riscv-random-asm = riscvmodel.random:gen_asm',
         'riscv-random-asm-check = riscvmodel.random:check_asm'
       ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)