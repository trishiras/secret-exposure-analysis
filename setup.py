from setuptools import setup, find_packages
from secret_exposure_analysis.__version__ import __version__


setup(
    name="secret_exposure_analysis",
    version=__version__,
    author="sumit",
    author_email="sumit@mail.com",
    description="secret-exposure-analysis",
    long_description=open("README.md").read(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.12",
    packages=find_packages(exclude=["config"]),
    entry_points={
        "console_scripts": [
            "secret_exposure_analysis=secret_exposure_analysis.main:main",
        ],
    },
)
