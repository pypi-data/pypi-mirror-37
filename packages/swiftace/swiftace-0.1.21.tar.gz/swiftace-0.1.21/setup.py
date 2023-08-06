import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swiftace",
    version="0.1.21",
    author="Aakash N S (SwiftAce)",
    author_email="opensource@swiftace.ai",
    entry_points={
        'console_scripts': ['swiftace=swiftace.cli:main'],
    },
    description="SwiftAce Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://swiftace.ai/",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=['tqdm', 'tuspy', 'requests']
)
