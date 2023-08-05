import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dorian',
    version='0.0.1',
    author='Sergey Redyuk',
    author_email='sergred@gmail.com',
    url='http://github.com/sergred/dorian',
    description='A tool for Data-Oriented experiment Reproducibility, Inspection and AutomatioN',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License 2.0',
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Science/Research"
    ],
    zip_safe=False
)
