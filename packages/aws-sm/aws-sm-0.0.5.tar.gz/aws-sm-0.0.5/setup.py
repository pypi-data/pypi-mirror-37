import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='aws-sm',
    version='0.0.5',
    author='jumpyoshim',
    author_email='jumpyoshim@gmail.com',
    description='A Python wrapper around the AWS Secrets Manager using Boto3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jumpyoshim/aws-sm',
    python_requires='>=3.5',
    install_requires=[
        'boto3==1.9.23',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
