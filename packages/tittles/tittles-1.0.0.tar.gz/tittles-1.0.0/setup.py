import setuptools

with open("README.md", "r") as readme_:
    long_description = readme_.read()

setuptools.setup(
    name="tittles",
    version="1.0.0",
    author="Leon",
    author_email="le_ma_@mail.ru",
    description="A package with a lot smal helpful things",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leonmaks/tittles",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
