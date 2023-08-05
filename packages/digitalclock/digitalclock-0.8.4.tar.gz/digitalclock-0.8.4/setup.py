import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="digitalclock",
    version="0.8.4",
    author="Juan Carlos Perez Castellanos",
    author_email="cuyopc@gmail.com",
    description="Seven segment display digital clock using Python tkinter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/johncharlie/digitalclock",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: Microsoft :: Windows",
    ],
    
)