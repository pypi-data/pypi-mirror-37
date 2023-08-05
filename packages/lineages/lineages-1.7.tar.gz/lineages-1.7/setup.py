import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lineages",
    version="1.7",
    author="Mobile Developers of Berkeley",
    author_email="kevin.jiang@berkeley.edu",
    description="A listing of all the lineages and class rosters of Mobile Developers of Berkeley",
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=["bin/lineages"],
    url="https://github.com/kevjiangba/FamilyTreeVisualizer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)