import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='flapp',
    version='0.0.1',
    author='Iakov Gnusin',
    author_email='y.gnusin@gmail.com',
    description='Flask application framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ignusin/flapp',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)