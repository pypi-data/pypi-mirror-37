import io
import os.path as op

from setuptools import setup, find_packages

here = op.abspath(op.dirname(__file__))

# Get the long description from the README file
with io.open(op.join(here, 'README.md'), mode='rt', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='text_classifier_kv',
    version='0.0.6',
    description='text classifier',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kopylovvlad/text_classifier_kv',
    author='Vladislav Kopylov',
    author_email='kopylov.vlad@gmail.com',
    packages=find_packages(),
    python_requires='>=3.5',
)
