import setuptools


with open('requirements.txt') as f:
    reqs = f.read().splitlines()

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='eeyore-nlp',
    version='0.0.11',
    description='',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires=reqs,
    long_description=long_description,
    long_description_content_type='text/markdown',
)