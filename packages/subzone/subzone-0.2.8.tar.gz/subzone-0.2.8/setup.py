import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="subzone",
    version="0.2.8",
    author="Nathan Corbin",
    author_email="ncorbuk@gmail.com",
    description="Subdomains,Dns records, & More!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ncorbuk/SubZone",
    packages=setuptools.find_packages(),
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt',]
        },
    install_requires=[
        'urllib3==1.22',
        'requests==2.18.4',
        'colorama==0.3.9',
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'subzone = subzone.main',
            # more script entry points ...
        ],
    }
)