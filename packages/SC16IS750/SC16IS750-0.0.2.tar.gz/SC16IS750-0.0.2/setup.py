import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SC16IS750",
    version="0.0.2",
    author="Harri Renney",
    author_email="harri.renney@blino.co.uk",
    description="Python driver for interfacing with SC16IS750 I2C chip",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Harri-Renney/SC16IS750.git",
    packages=setuptools.find_packages()
)
