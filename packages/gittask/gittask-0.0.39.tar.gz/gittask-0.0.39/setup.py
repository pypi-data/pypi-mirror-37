import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'VERSION')
          ) as version_file:
    version = version_file.read().strip()

setuptools.setup(
    name="gittask",
    version=version,
    author="bessbd",
    author_email="bessbd@gmail.com",
    description="Git-task",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bessbd/gittask",
    packages=setuptools.find_packages(),
    install_requires=[
        "fire",
        "pyyaml",
    ],
    data_files=[
        ('', ['VERSION']),
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
