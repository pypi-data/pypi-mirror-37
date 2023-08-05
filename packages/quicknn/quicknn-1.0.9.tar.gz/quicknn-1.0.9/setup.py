import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

params = dict(
    name="quicknn",
    version="1.0.9",
    author="Lorenzo Palloni",
    author_email="palloni.lorenzo@gmail.com",
    description="An implementation of Feedforward Neural Networks for quick applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/deeplego/quicknn",
    py_modules=["quicknn", "qnn_config"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
if __name__ == "__main__":
    setuptools.setup(**params)

