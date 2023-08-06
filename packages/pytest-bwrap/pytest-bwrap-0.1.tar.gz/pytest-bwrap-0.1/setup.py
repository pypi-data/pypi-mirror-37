from pathlib import Path
from setuptools import find_packages, setup


README = Path('README.rst').read_text()
CHANGES = Path('CHANGES.rst').read_text()


setup(
    name='pytest-bwrap',
    description='Run your tests in Bubblewrap sandboxes',
    long_description='%s\n\n%s' % (README, CHANGES),
    version='0.1',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        ('License :: OSI Approved :: GNU Lesser General Public License v3 or '
         'later (LGPLv3+)'),
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Testing',
    ],
    author='Mathieu Bridon',
    author_email='bochecha@daitauha.fr',
    url='https://framagit.org/bochecha/pytest-bwrap/',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pytest',
    ],
    entry_points={
        'pytest11': [
            'pytest-bwrap = pytest_bwrap',
        ],
    },
)
