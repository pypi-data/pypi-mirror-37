import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EpitechApi",
    version="0.0.1",
    author="Erwan Bernard",
    author_email="erwan.bernard079@gmail.com",
    description="A small wrapper for Epitech Api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kyashar/EpitechPythonApi",
    packages=["EpitechApi"],
    install_requires = [
      'requests>=2.19.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
