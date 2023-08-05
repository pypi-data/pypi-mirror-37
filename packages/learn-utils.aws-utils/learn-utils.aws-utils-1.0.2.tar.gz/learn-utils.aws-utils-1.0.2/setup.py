from setuptools import setup, find_packages
# builds the project dependency list
install_requires = None
with open('requirements.txt', 'r') as f:
        install_requires = f.readlines()

# setup function call
setup(
    name="learn-utils.aws-utils",
    version="1.0.2",
    author="Luis Felipe Muller",
    author_email="luisfmuller@gmail.com",
    description=("A collection of common aws code."),
    keywords="logger, boto3, sqs, s3",
    # Install project dependencies
    install_requires=install_requires,

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.md', "*.json", "*.zip"],
    },
    include_package_data=True,
    packages=find_packages(exclude=["*tests"])
)
