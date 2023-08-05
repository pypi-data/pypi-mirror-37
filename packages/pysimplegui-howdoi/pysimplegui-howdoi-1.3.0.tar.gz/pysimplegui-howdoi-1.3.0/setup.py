import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysimplegui-howdoi",
    version="1.3.0",
    author="PySimpleGUI.org",
    author_email="info@PySimpleGUI.org",
    description="A GUI Front-end to How Do I",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['howdoi', 'pysimplegui'],
    url="https://github.com/MikeTheWatchGuy/PySimpleGUI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows ",
    ],
)