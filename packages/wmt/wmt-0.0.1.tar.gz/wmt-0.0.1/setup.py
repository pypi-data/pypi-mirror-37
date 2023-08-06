import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wmt",
    version="0.0.1",
    author="IdanP",
    author_email="idan.kp@gmail.com",
    description="Where is my time?",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idanp/wmt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
