import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='elasticbeanstalk-to-env',
    version='0.1',
    author="Jason DeWitt",
    author_email="jason.dewitt@10up.com",
    description="A simple tool that exports ElasticBeanstalk envrionment variables to a .env file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'Click',
        'boto3',
        'future',
        'future-fstrings',
    ],
    entry_points='''
        [console_scripts]
        eb-to-env=eb_to_env.main:cli
    ''',
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)