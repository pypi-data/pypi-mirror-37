import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PySimpleGUI-chess",
    version="0.0.3",
    author="PySimpleGUI.org",
    author_email="info@PySimpleGUI.org",
    description="A PGN file playback of chess games",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['python-chess', 'pysimplegui'],
    package_data={
        'PySimpleGUI-chess': ['*.png', '*.pgn'],
                },
    url="https://github.com/MikeTheWatchGuy/PySimpleGUI/tree/master/Chess",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)