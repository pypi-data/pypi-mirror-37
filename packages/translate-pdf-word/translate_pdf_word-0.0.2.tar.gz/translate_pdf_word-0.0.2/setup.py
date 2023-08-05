import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="translate_pdf_word",
    version="0.0.2",
    author="Yanfeng Wu",
    author_email="yanfeng1223@126.com",
    description="A package for translating pdf or word files into Chinese versions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xmlongan/translate-pdf-word",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
