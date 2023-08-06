import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wyliozero",
    version="0.0.20",
    author="Serban Razvan",
    author_email="razvan.serban@wyliodrin.com",
    description="Library for Wyliodrin Lab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Wyliodrin/wyliozero",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Topic :: Education"
    ],
)
