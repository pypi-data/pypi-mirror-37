import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements/prod.txt", "r") as fh:
    requirements = [l.split() for l in fh.readlines()]

setuptools.setup(
    name="split-gzip-upload-tool",
    version="0.0.1",
    author="Andrii Stepaniuk",
    author_email="andrii.stepaniuk@gmail.com",
    description="Tool to split stdin, gzip it and upload to s3",
    url="https://github.com/andriis/split-gzip-upload-tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'split-gzip-upload = split_gzip_upload.tool:main',
            'sgu = split_gzip_upload.tool:main',
        ],
    },
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    )
)
