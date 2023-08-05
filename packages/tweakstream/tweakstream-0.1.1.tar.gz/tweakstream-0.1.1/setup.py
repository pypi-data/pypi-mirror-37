from setuptools import setup

from tweakstream import __version__


with open("README.md") as f:
    readme = f.read()

with open("requirements.txt") as f:
    requirements = f.read().split()

setup(
    name="tweakstream",
    version=__version__,
    description="Tweakers topic streamer",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/timotk/tweakstream",
    packages=['tweakstream'],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={"console_scripts": ["tweakstream = tweakstream.cli:cli"]},
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
