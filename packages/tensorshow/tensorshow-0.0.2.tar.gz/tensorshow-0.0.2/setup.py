import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tensorshow",
    version="0.0.2",
    author="Joel Laity",
    author_email="joel.laity@gmail.com",
    description="A python module and commaned line tool for inspecting TFRecords.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joelypoley/tensorshow",
    # Doesn't work because of setuptools problems.
    # scripts=['bin/tensorshow'],
    packages=setuptools.find_packages(),
    install_requires=["fleep", "ipython", "pandas", "pillow", "tensorflow"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
