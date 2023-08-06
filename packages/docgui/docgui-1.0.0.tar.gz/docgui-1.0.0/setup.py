import setuptools


with open("PYPI_README.md", 'r') as f:
    readme = f.read()


setuptools.setup(
    name="docgui",
    version="1.0.0",
    entry_points={
        'console_scripts': []
    },
    packages=setuptools.find_packages(),
    install_requires=[],
    author='Armand Foucault',
    author_email='armand.foucault@telecom-bretagne.eu',
    description="Turn docopt programs into GUI applications",
    long_description=readme,
    long_description_content_type='text/markdown',
    url="https://github.com/Afoucaul/docgui"
)
