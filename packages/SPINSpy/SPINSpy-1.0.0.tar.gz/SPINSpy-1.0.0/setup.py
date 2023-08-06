import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SPINSpy",
    version="1.0.0",
    author="Ben Storer",
    author_email="bastorer@uwaterloo.ca",
    description="A set of python tools for processing SPINS outputs.",
    url="https://git.uwaterloo.ca/bastorer/SPINSpy",
    project_urls={
        'Documentation' : 'https://git.uwaterloo.ca/bastorer/SPINSpy/wikis/home',
        'Source' : 'https://git.uwaterloo.ca/bastorer/SPINSpy',
        },
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
