import io  # for python2
from os import path
from setuptools import setup, find_packages
from ickafka.__version__ import version

WORKING_DIR = path.abspath(path.dirname(__file__))

# Get long description from README.md
with io.open(path.join(WORKING_DIR, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    author="Dave Gallant",
    description="Improved Color Kafka",
    entry_points={"console_scripts": ["ickafka=ickafka.app:main"]},
    install_requires=["kafka-python>=1.3.1", "pygments>=2.2.0"],
    keywords=["kafka", "pygments"],
    license="Apache License, Version 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="ickafka",
    packages=find_packages(),
    url="https://github.com/davegallant/ickafka",
    version=version,
)
