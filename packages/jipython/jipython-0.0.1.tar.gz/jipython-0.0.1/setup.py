import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jipython",
    version="0.0.1",
    author="ji",
    author_email="ji.zhou@example.com",
    description="A test install package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/jipythonproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
