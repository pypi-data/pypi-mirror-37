from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

requires = [
    'exifread',
    'Pillow',
    'pathlib',
]

setup(
    name="someutils",
    version="0.4.3",
    author="flow.gunso",
    author_email="flow.gunso@gmail.com",
    description="Various utilities for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/flow.gunso/someutils",
    packages=find_packages(),
    install_requires=requires,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System",
        "Topic :: Utilities",
    ],
)
