import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bredon",
    version="1.0.5",
    author="Simon Chervenak",
    author_email="simonlcherv@gmail.com",
    description="A set of tools for the game Tak.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Innoviox/bredon",
    packages=setuptools.find_packages(),
    license="GNU General Public License v3.0",
    install_requires=['dataclasses==0.4',
                      'tabulate==0.8.2',
                      'click==7.0',
                      'gym==0.10.8',
                      'tqdm==4.26.0']
)