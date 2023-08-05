import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="disguise",
    version="0.0.1",
    author="Artem Likhvar",
    author_email="me@a10r.com",
    description="Initial stub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitlab/a10r/disguise",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
