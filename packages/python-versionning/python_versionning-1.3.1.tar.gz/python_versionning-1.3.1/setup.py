import setuptools


with open("PYPI_README.md", 'r') as f:
    readme = f.read()


setuptools.setup(
    name="python_versionning",
    version="1.3.1",
    entry_points={
        'console_scripts': []
    },
    packages=setuptools.find_packages(),
    install_requires=[],
    author='Armand Foucault',
    author_email='armand.foucault@telecom-bretagne.eu',
    description="Manage your projects' version",
    long_description=readme,
    long_description_content_type='text/markdown',
    url="https://github.com/Afoucaul/pyver"
)
