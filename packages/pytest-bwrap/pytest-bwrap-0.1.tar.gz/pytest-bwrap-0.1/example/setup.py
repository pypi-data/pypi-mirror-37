from setuptools import find_packages, setup


setup(
    name='example',
    description="A quick example of how to use pytest-bwrap",
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)
