import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="runana",
    version="0.1.1",
    author="Jens Svensmark",
    author_email="jenssss@uec.ac.jp",
    # description = ("An demonstration of how to create, document, and publish "
    #                                "to the cheese shop a5 pypi.org."),
    # license = "BSD",
    keywords="run analyse",
    # url = "http://packages.python.org/an_example_pypi_project",
    packages=['runana'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
    ],
)
