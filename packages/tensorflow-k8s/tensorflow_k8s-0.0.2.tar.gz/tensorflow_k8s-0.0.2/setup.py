import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tensorflow_k8s",
    version="0.0.2",
    author="Kundjanasith Thonglek",
    author_email="kundjanasith.t@Ku.th",
    description="Tensorflow serving extension",
    long_description=". . .",
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/tensorflow_k8s",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Academic Free License (AFL)",
        "Operating System :: OS Independent",
    ],
)


