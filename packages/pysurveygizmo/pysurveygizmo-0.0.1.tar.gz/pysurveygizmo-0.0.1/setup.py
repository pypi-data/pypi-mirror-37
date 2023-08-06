import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysurveygizmo",
    version="0.0.1",
    author="Courtney Ferguson Lee",
    author_email="cfergusonlee@venturewell.org",
    description="A package for Survey Gizmo that pulls response and campaign data using your account API key and a valid survey ID number, returning a Pandas dataframe.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/venturewell/pysurveygizmo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)