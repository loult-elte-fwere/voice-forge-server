# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from pathlib import Path

here = Path(__file__).parent.absolute()

# Get the long description from the README file
with open(here / Path('README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='loult-voice-forge',
    version='0.1.0',
    description='An API for the Loult\'s voice creation API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    author='hadware',
    license="AGLP",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='',
    namespace_packages=['voice_forge'],
    packages=find_packages(),
    setup_requires=['setuptools>=38.6.0'],  # >38.6.0 needed for markdown README.md
    tests_require=['pytest'],
    entry_points={
        'console_scripts': []
    }
)
