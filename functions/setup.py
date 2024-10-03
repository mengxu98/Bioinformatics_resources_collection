from setuptools import setup
import pathlib

from functions.version import __version__

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="Bioinformatics_resources_collection",
    version=__version__,
    description="This tool is used to auto record paper information.",
    url="https://github.com/mengxu98/Bioinformatics_resources_collection",
    author="Alan Shi",
    author_email="mengxu98@qq.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["Bioinformatics_resources_collection"],
    python_requires=">=3.7",
    project_urls={  # Optional
        "Bug Reports": "https://github.com/mengxu98/Bioinformatics_resources_collection/issues",
        "Source": "https://github.com/mengxu98/Bioinformatics_resources_collection/",
    },
)
