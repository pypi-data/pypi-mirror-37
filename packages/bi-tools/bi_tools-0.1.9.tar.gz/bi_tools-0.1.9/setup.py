import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bi_tools",
    version="0.1.9",
    author="BI Data Engineering",
    author_email="jun.kim@pitchbook.com",
    description="PitchBook Business Intelligence Python Toolbox",
    url="https://git.pitchbookdata.com/business-intelligence/bi_tools",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
