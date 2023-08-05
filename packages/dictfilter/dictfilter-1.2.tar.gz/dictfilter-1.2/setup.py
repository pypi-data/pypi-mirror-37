import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='dictfilter',
    version='1.2',
    author='Chris Latham',
    author_email='backwardspy@gmail.com',
    description='Filter dictionaries based on a list of field names.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://git.bink.com/libs/dictfilter',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
