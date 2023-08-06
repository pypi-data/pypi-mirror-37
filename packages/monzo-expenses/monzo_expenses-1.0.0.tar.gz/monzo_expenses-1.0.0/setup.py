import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="monzo_expenses",
    version="1.0.0",
    author="Sam Dobson",
    author_email="sjd333@gmail.com",
    description="Generate expense reports from Monzo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samdobson/monzo-expenses",
    install_requires=[
      'weasyprint'
    ],
    include_package_data=True,
    packages=setuptools.find_packages(),
    scripts=['bin/monzo-expenses'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
