import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unsplash_search",
    version="0.2.0",
    author="Orlando Diaz",
    author_email="orlandodiaz.dev@gmail.com",
    description="Search unsplash for photos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orlandodiaz/unsplash_search",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = ['requests>=2.19.1', 'log3>=0.1.6']

)