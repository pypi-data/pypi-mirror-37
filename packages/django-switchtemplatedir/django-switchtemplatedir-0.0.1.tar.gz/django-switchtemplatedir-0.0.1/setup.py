import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-switchtemplatedir",
    version="0.0.1",
    author="Hayk Manukyan",
    author_email="haykhman@gmail.com",
    description="Django middleware - symply switch template dir",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haykhman/django-switchtemplatedir",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          
    ],
)

