import versioneer
from setuptools import setup


with open('README.rst', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt') as fh:
    requirements = fh.readlines()

setup(
    name='docser',
    packages=['docser'],
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='A simple server for hosting Sphinx documentation',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Chris Brake',
    author_email='chris.brake@gmail.com',
    url='https://github.com/chrisbrake/docser',
    keywords=['docser', 'Sphinx', 'documentation'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ],
    install_requires=requirements
)
