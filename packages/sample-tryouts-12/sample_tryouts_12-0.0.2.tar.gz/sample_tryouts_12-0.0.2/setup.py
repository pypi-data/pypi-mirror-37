import setuptools

setuptools.setup(
    name="sample_tryouts_12",
    version="0.0.2",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description="This is a very long description",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests'],
    extras_require={
        'test': ['pytest', 'pytest-runner', 'pytest-cov', 'pytest-pep8'],
    },
)
