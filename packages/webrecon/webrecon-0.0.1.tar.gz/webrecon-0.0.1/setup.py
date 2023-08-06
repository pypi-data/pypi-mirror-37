import setuptools
# google-api-python-client
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="webrecon",
    version="0.0.1",
    author="Adam Phillipps",
    author_email="adam.phillipps@gmail.com",
    description="Get information from various web resources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adam-phillipps/recon/tree/master/web_recon",
    packages=setuptools.find_packages(),
    install_requires=[
        'boto3',
        'google-api-python-client'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
