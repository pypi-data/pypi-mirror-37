import setuptools

with open('./README.md') as f:
    long_description = f.read()


setuptools.setup(
    name="webviz-petech",
    version="0.0.1",
    author="Equinor ASA",
    author_email="fg_gpl@equinor.com",
    description="Webviz petech provides webviz plugins related to specialized petech visualizations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Statoil/webviz_petech",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Bug Reports': 'https://github.com/Statoil/webviz_petech/issues',
},
)
