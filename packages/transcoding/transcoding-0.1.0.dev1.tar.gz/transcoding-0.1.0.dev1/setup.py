"""
Publishing:
    run tests
    remember to change the version in setup(... ) below
    $ git commit -am "<my message>"
    $ git push
    $ git tag -a v<my.version.id> -m "<comment to my version>"  # tag version
    $ git push origin v<my.version.id>  # explicitly push tag to the shared server
    $ python setup.py sdist
    $ twine upload dist/*

"""
from setuptools import setup, find_packages
exec(open("./transcoding/__about__.py").read())

setup(
    name=__title__,
    version=__version__,
    description=__summary__,
    author=__author__,
    author_email=__email__,
    license=__license__,
    keywords=__keywords__,
    packages=find_packages(),
    url=__uri__,
    project_urls={
        'Documentation': __uri__,
        'Source': __uri__,
    },
    test_require=[
        'doctest',
        'unittest'
    ],
    install_requires=[
        'parse',
        'more_itertools',
    ],
    entry_points={
        'console_scripts': ['transcoding = transcoding.__main__:runDoctests']
    },
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    python_requires='>=2.7',
)


# in the terminal:
# pip install .
