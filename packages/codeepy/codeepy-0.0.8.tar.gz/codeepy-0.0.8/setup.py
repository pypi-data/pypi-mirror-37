import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codeepy",
    version="0.0.8",
    author="Marita Fitzgerald",
    author_email="maritafitzgerald@gmail.com",
    description="A library for the Codee Robot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mefitzgerald/CodeePy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
	install_requires=[
   'pyfirmata',
   'pyserial'
	],
)