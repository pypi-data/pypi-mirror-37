import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cdmon_automator",
    version="0.0.4",
    author="Develatio",
    author_email="contact@develat.io",
    description="Library for CRUD operations on cdmon.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/develatio/cdmon_automator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Systems Administration"
    ],
    install_requires=[
        "selenium",
        "python-decouple",
        "chromedriver_binary"
    ]
)