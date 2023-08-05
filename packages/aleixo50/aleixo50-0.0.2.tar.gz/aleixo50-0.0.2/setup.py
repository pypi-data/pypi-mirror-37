import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aleixo50",
    version="0.0.2",
    author="André Santos",
    author_email="andrefs@andrefs.com",
    description="Bruno Aleixo's famous 50 Portuguese traditional dishes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrefs/python-aleixo50",
    packages=setuptools.find_packages(),
    scripts=['bin/aleixo50'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Utilities"
    ],
)
