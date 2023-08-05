import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="myFirstPiPy",
    version="0.0.1",
    author="Daniel Bunzendahl",
    author_email="StudentDanBu@gmail.com",
    description="My first PiP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StudentESE/myFirstPiP",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)