import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="android_category",
    version="0.0.3",
    author="Luis Cruz",
    author_email="luismirandacruz@gmail.com",
    description="Tool to retrieve the category of an app given a url to the source code (git/local).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luiscruz/android_category",
    packages=setuptools.find_packages(),
    install_requires=[
        "Click==7.0",
        "GitPython==2.1.11",
        "google_play_reader>=0.0.1.dev16",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['android_category=android_category.cli:tool'],
    },
)