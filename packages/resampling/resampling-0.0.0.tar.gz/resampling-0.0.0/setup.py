from setuptools import setup, find_packages

import resampling

setup(
    name="resampling",
    version=resampling.__version__,
    packages=sorted(find_packages(exclude=("*.tests",))),
    url="https://github.com/artemmavrin/resampling",
    author='Artem Mavrin',
    author_email="amavrin@ucsd.edu",
    description="Resampling techniques and associated statistical inference",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ]
)
