import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fcem",
    version="0.0.1",
    author="Cycle ML Team",
    author_email="ml@cyclesystem.org",
    description="Fuzzy Comprehensive Evaluation Methodology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cycle-system/fcem",
    packages=setuptools.find_packages(),
    install_requires=[
          'numpy',
	  'scikit-fuzzy', 	
	  'scikit-learn==0.19'	
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
