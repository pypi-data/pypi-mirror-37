import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="inside",
    version="0.0.3",
    author="William Wyatt",
    author_email="wwyatt@ucsc.edu",
    description="Collision detection with polygons.",
    long_description="Collision detection with polygons.",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/Tsangares/overlap",
    #package_data={'lgad': ['plates.json']},
    scripts=['inside/parse.py'],
    #install_requires=["matplotlib", "numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
