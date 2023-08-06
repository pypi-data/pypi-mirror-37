import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ndip_checker",
    version="1.0.2a4",
    author="Yarving Liu",
    author_email="yarving@gmail.com",
    description="check and fix errors in NDIP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/yarving/NdipChecker",
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': [
            'ncheck=ndip_checker:execute_from_command_line',
    ]},
    install_requires=['MySQL-python'],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
