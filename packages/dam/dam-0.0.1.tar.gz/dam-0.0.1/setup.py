from setuptools import setup

with open("README.md") as file:
    long_desc = file.read()

setup(
    name="dam",
    author="BigHeadGeorge",
    url="https://github.com/BigHeadGeorge/dam",
    version="0.0.1",
    packages=['dam'],
    zip_safe=True,
    description="A simple package for managing Discord dev applications.",
    long_description=long_desc,
    long_description_content_type='text/markdown',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Internet"
    ]
)
