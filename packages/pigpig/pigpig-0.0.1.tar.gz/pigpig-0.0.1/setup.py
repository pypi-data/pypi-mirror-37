import os
import sys
import io
import re
from setuptools import setup


# "setup.py publish" shortcut.
if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist')
    os.system('twine upload dist/*')
    os.system('rm -rf dist pigpig.egg-info')
    sys.exit()

with io.open("pigpig/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \'(.*?)\'", f.read()).group(1)

def check_dependencies():
    install_requires = []
    try:
        import numpy
    except ImportError:
        install_requires.append('numpy')
    try:
        import numba
    except ImportError:
        install_requires.append('numba')
    return install_requires

setup(
    name='pigpig',
    version=version,
    description="A naive & useless deep learning framework.",
    keywords='deep-learning',
    author='Zheng Zhou',
    author_email='yootaoo@gmail.com',
    url='https://github.com/zhoudaxia233/PigPig',
    license='MIT',
    packages=['pigpig'],
    include_package_data=True,
    zip_safe=False,
    install_requires=check_dependencies(),
    python_requires='>=3.6',
    dependency_links=[]
)
