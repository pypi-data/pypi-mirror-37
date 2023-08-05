import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="palombe",
    version="0.2.0",
    author="Yvan Sraka",
    author_email="yvan@sraka.pw",
    description="Palombe lets you send and receive messages synchronously through different processes using named pipes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/yvan-sraka/palombe-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Unix",
    ],
)

