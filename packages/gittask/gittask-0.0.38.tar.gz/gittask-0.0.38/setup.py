import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gittask",
    version="0.0.38",
    author="bessbd",
    author_email="bessbd@gmail.com",
    description="Git-task",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bessbd/gittask",
    packages=setuptools.find_packages(),
    install_requires=[
        "fire",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'gittask = gittask.GitTask:main'
        ],
    },
)
