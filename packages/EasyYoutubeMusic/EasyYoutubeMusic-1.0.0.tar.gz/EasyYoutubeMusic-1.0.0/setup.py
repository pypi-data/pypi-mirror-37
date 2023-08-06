import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="EasyYoutubeMusic",
    version="1.0.0",
    author="Nenad Bauk",
    author_email="bauk.nenad@gmail.com",
    description="Python command-line tool to download your YouTube music.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fifiman/EasyYoutubeMusic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent",
    ],
)