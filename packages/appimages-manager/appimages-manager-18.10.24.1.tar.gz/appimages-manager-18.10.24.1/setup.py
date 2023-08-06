import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="appimages-manager",
    version="18.10.24.1",
    author="Kaiser",
    author_email="kylebell68@gmail.com",
    description="Simplistic tools for managing appimages with little effort.",
    long_description=long_description,
    scripts=['bin/aim'],
    long_description_content_type="text/markdown",
    url="https://github.com/Kaiz0r/AppImages-Manager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX :: Linux",
    ],
)
