from setuptools import setup, find_packages

setup(
    description="Python Library for Handling Dynamo Syntax and requests.",
    author="Barry Howard",
    author_email="barry.howard@ge.com",
    url="https://github.build.ge.com/Cloudpod/pynamo",
    version="1.2.1539725855",
    keywords=[u'dynamo', u'ge', u'cloudops', u'aws'],
    name="pynamo",
    packages=find_packages(exclude=["build", "build/*"])
)
