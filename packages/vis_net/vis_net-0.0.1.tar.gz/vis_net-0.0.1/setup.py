import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vis_net",
    version="0.0.1",
    author="kurumi",
    author_email="935211204@qq.com",
    description="A small vis package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cryer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)