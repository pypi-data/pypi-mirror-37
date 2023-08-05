import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="social_core_optimized",
    version="0.0.1",
    author="Marcio Alfredo",
    author_email="marcio.alfredo1@gmail.com",
    description="A optimization of social_django_auth",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marciojunior/social-core-optimized",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
