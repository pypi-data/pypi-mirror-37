import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pythonUtility",
    version="0.2.0",
    author="Joel Widmer",
    author_email="joel.widmer.wj@gmail.com",
    description="Python utility collection",
    license="BSD",
    keywords="Utilities",
    url="https://git.widmer.me/project/pythonUtil",
    packages=[
        "pythonUtils"
    ],
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
