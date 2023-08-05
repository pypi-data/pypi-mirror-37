import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='csvkey',
    version='0.0.3',
    author='KOBAYASHI Ittoku',
    author_email='nono381d815@gmail.com',
    description='use PRIMARY KEY and UNIQUE in CSV',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kittoku/csvkey',
    packages=setuptools.find_packages(),
    install_requires=['pandas', 'pyyaml'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
