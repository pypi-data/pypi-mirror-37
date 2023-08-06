import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deepmg",
    version="0.2.4",
    author="Thanh-Hai Nguyen",
    author_email="hainguyen579@gmail.com",
    description="A python package to visualize data using machine/deep learning algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.integromics.fr/published/deepMG_tf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
