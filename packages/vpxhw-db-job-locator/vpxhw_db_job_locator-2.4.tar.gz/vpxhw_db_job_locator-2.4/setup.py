import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='vpxhw_db_job_locator',
    version='2.4',
    author='Ray Xu',
    author_email='rxuniverse@google.com',
    description="package for locating jobs in vpxhw database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['Jinja2', 'requests',],
    setup_requires=["pytest-runner",],
    tests_require=["pytest", "mock",
"PyHamcrest",
"testfixtures",],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)