import setuptools

with open("README.md", "r") as fh:
        long_description = fh.read()

        setuptools.setup(
                    name="magician_package",
                    version="0.3.31",
                    author="RAISE_LAB",
                    author_email="smajumd3@ncsu.edu",
                    description="A small example package for text mining application with hyper-parameter optimization on multiple learning to automatically find best model",
                    long_description=long_description,
                    long_description_content_type="text/markdown",
                    url="https://github.com/ai-se/magician_package",
                    packages=setuptools.find_packages(),
                    classifiers=[
                        "Programming Language :: Python :: 2.7",
                        "License :: OSI Approved :: MIT License",
                        "Operating System :: OS Independent",
                    ],
        )
