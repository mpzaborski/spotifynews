import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spotifynews",
    version="0.1.1",
    author="Mateusz Zaborski",
    author_email="mpzaborski@gmail.com",
    description="Spotify news",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mpzaborski/spotifynews",
    install_requires=[
        'atomicwrites>=1.4.0',
        'attrs>=20.3.0',
        'certifi>=2020.12.0'
        'chardet>=4.0.0',
        'colorama>=0.4.0'
        'idna>=2.10',
        'iniconfig>=1.1.0',
        'packaging>=20.9',
        'pluggy>=0.13.0',
        'py>=1.10.0',
        'pyparsing>=2.4.7',
        'requests>=2.25.0',
        'six>=1.15.0',
        'spotipy>=2.16.1',
        'toml>=0.10.0',
        'urllib3>=1.26.0'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
