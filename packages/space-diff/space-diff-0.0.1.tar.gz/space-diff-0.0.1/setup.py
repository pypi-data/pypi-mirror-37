import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="space-diff",
    version="0.0.1",
    author="Blake Perry Smith",
    author_email="perry.smithb@gmail.com",
    description="A tool that highlights inconsistencies in word segmentation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smithnlp/space-diff",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
