import setuptools

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except:
    pass

setuptools.setup(
    name="bi_s3",
    version="0.2.2",
    author="BI Data Engineering",
    author_email="jun.kim@pitchbook.com",
    description="S3 connector package designed to make data lake operations easier for PitchBook Business Intelligence",
    url="https://git.pitchbookdata.com/business-intelligence/bi_s3",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
