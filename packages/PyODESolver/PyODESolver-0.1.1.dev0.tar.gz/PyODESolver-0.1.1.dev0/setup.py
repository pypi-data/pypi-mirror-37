import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='PyODESolver',  # This is the name of your PyPI-package.
    version='0.1.1.dev',  # Update the version number for new releases
    author='C. Hoeppke, A. Puiu',
    author_email='christoph.hoeppke@maths.ox.ac.uk',
    description='A python package to solve first order ODEs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Hoeppke/PyODESolver',
    packages=setuptools.find_packages(),
    licence='MIT license',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
