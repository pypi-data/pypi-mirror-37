import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sunlite",
    version="0.5.0",
    author="Sun",
    author_email="sun600@outlook.com",
    description="A simple database system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://sunx2.github.io/sunlite/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
   'flask-restful',
   'flask'
],
)