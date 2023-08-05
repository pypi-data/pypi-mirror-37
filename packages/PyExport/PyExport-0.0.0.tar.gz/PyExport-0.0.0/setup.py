import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyExport",
    version="0.0.0",
    author="Sonal Raj",
    author_email="sonal.nitjsr@gmail.com",
    description="Export data programatically to emails, html, pdf, docs, xls, etc.",
    long_description="Export data programatically to emails, html, pdf, docs, xls, etc.",
    long_description_content_type="text/markdown",
    url="https://github.com/sonal-raj/PyExport",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)