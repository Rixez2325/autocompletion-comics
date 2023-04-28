import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()


setuptools.setup(
    name="autocompletion-comics",
    version="0.0.1",
    author="Marvin CHERRIERE, Florent COMPAGNONI, Daoud HANDAS",
    author_email="mcherriere.pro@gmail.com, florent.compagnoni+dev@gmail.com, daoudhandas@gmail.com",
    description="Package used for comics generator app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    install_requires=requirements,
    python_requires=">=3.10",
)
