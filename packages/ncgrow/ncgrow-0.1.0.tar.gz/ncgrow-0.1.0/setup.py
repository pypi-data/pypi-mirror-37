from setuptools import setup, find_packages

setup(
    name='ncgrow',
    version='0.1.0',
    scripts=['ncgrow.py'],
    packages=find_packages(),
    url='https://gitlab.com/FCOO/ncgrow',
    install_requires=[
        'netCDF4',
        'numpy'
    ],
    author = 'Brian Højen-Sørensen',
    author_email = 'brs@fcoo.dk',
    license='GPLv3'
)
