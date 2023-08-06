from setuptools import setup, find_packages

version='0.1.5'

setup(
    name = 'mprows',
    version = version,
    packages = ['mprows'],
    description = 'multiprocessing on row data using user defined functions',
    scripts = [],
    license='MIT',
    author = 'pipidog',
    author_email = 'pipidog@gmail.com',
    url = 'https://github.com/pipidog/mprows',
    download_url = 'https://github.com/pipidog/mprows/archive/v.'+version+'.tar.gz',
    keywords = ['multiprocessing','pathos','data cleaning'],
    classifiers = ['Topic :: Utilities'],
    install_requires=['numpy','pathos']
)
