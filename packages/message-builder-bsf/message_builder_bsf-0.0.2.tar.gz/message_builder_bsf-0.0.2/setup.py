import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="message_builder_bsf",
    version="0.0.2",
    author="Steven Wallimann",
    author_email="steven.wallimann@bibliosansfrontieres.org",
    description="Library used to build our messages for our Microservices platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bibliosansfrontieres/message_builder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
