
import os
from setuptools import setup, find_packages


VERSION = u'1.0.7'
NAME = u'misguided_xml'


def read(filename):

    """
    Utility function used to read the README file into the long_description.

    :param filename: Filename to read

    :return: file pointer
    """

    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name=NAME,  # The module name must match this!

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=VERSION,

    author=u"Hywel Thomas",
    author_email=u"hywel.thomas@mac.com",

    license=u'MIT',

    url=u'https://bitbucket.org/daycoder/misguided_xml.git',  # Use the url to the git repo
    download_url=(u'https://bitbucket.org/daycoder/'
                  u'misguided_xml.git/get/{version}.tar'
                  .format(version=VERSION)),

    packages=find_packages(),

    # If you want to distribute just a my_module.py, uncomment
    # this and comment out packages:
    #   py_modules=["my_module"],

    description=u"Read/Write/Create/Modify/Search/Format XML files..\n"
                u"Note that you should probably use ElementTree rather "
                u"than this. I wrote this while I was learning Python,"
                u"for shits and giggles. Adding what I needed as I "
                u"needed it. Turns out reinventing the wheel wasn't "
                u"the best idea, particularly as I have an aversion "
                u"regular expressions, meaning while there's searching, "
                u"it's not XPATH.",
    long_description=read(u'README.md'),

    keywords=[u'XML'],

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project?
        #   Development Status :: 1 - Planning
        #   Development Status :: 2 - Pre-Alpha
        #   Development Status :: 3 - Alpha
        #   Development Status :: 4 - Beta
        #   Development Status :: 5 - Production/Stable
        #   Development Status :: 6 - Mature
        #   Development Status :: 7 - Inactive
        u'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        u'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        u'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        u'Programming Language :: Python :: 2',
        u'Programming Language :: Python :: 2.7',

        u'Topic :: Utilities',
    ],

    # Dependencies
    install_requires=[
        u'future>=0.16.0',
        u'fdutil>=1.2.2',
        u'conversionutil>=1.4.1'
    ],

    # Reference any non-python files to be included here
    package_data={
        '': ['*.md', '*.rst', '*.db', '*.txt'],  # Include all files from any package that contains *.db/*.md/*.txt
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [],
    },

    # List any scripts that are to be deployed to the python scripts folder
    scripts=[]

)
