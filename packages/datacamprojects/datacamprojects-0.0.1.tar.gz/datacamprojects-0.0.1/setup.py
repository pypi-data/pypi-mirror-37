import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datacamprojects",
    version="0.0.1",
    author="Martin Skarzynski",
    author_email="marskar@gmail.com",
    description="Tools for the DataCamp Creating Robust Python Projects course",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marskar/datacamprojects",
    packages=['src'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'datacamprojects = datacamprojects.__main__:main'
        ]
    },
    install_requires=[
        'scikit-learn',
        'matplotlib',
        'seaborn'
    ]
)