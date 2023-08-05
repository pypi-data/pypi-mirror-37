import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_camel_field",
    version="0.0.1",
    author="Ivan Zhang",
    author_email="sail4dream@gmail.com",
    description="ForeignKey/OneToOneField with Camel Case Attribute Name",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhangi/django_camel_field",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
