import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="space-diff",
    version="0.0.6",
    author="Blake Perry Smith",
    author_email="perry.smithb@gmail.com",
    description="A tool that highlights inconsistencies in word segmentation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smithnlp/space-diff",
    keywords=[
        'chinese',
        'japanese',
        'word segmentation',
        'corpus linguistics',
        'consistency'],
    packages=setuptools.find_packages(),
    install_requires=['progress'],
    python_requires='~=3.7',
    scripts=['bin/space-diff'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
