import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="novel-dehtml",
    version="0.0.7",
    author="Willian Z.",
    author_email="willian@willian-zhang.com",
    description="Decode HTML in novel text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/willian-zhang/novel-dehtml",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # scripts=['bin/novel-dehtml'],
    entry_points = {
        'console_scripts': ['novel-dehtml=dehtml.main:main'],
    }
)