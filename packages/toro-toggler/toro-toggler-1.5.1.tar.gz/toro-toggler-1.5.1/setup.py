import os

from setuptools import setup, find_packages

here =      os.path.abspath(os.path.dirname(__file__))
readme =    open(os.path.join(here, 'README.rst')).read()
changes =   open(os.path.join(here, 'CHANGES.rst')).read()

requires = []

setup(
    name='toro-toggler',
    version='1.5.1',
    description="TORO python markdown extension for wrapping image in special div tag",
    long_description="{readme}\n\n{changes}".format(readme=readme, changes=changes),
    classifiers=[
        "Programming Language :: Python",
    ],
    author='Jerrick M. Pua',
    author_email='jerrick.pua@toro.io',
    keywords='python toro',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='toro-toggler',
    install_requires = requires,
)
