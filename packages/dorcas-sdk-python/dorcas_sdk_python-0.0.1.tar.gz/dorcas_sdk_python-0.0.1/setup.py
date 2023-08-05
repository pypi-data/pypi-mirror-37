import setuptools

with open('README.md', 'r') as handle:
    description = handle.read()


setuptools.setup(
    name="dorcas_sdk_python",
    version="0.0.1",
    author="Emmanuel Okeke",
    author_email="emmanix2002@gmail.com",
    description="A Python wrapper for communicating with the Dorcas API",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/dorcasng/dorcas-sdk-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)