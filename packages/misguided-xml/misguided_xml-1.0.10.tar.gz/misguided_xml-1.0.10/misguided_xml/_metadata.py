# encoding: utf-8

# Variables for setup (these must be string only!)
__module_name__ = u'misuided_xml'
__description__ = (u"Read/Write/Create/Modify/Search/Format XML files..\n"
                   u"Note that you should probably use ElementTree rather "
                   u"than this. I wrote this while I was learning Python,"
                   u"for shits and giggles. Adding what I needed as I "
                   u"needed it. Turns out reinventing the wheel wasn't "
                   u"the best idea, particularly as I have an aversion "
                   u"regular expressions, meaning while there's searching, "
                   u"it's not XPATH.")

__version__ = u'1.0.10'

__author__ = u'Hywel Thomas'
__authorshort__ = u'HT'
__authoremail__ = u'hywel.thomas@mac.com'

__license__ = u'MIT'

__githost__ = u'bitbucket.org'
__gituser__ = u'daycoder'
__gitrepo__ = u'cachingutil.git'


# Additional variables
__copyright__ = u'Copyright (C) 2016 {author}'.format(author=__author__)

__url__ = u'https://{host}/{user}/{repo}'.format(host=__githost__,
                                                 user=__gituser__,
                                                 repo=__gitrepo__)
__downloadurl__ = u'{url}/get/{version}.tar'.format(url=__url__,
                                                    version=__version__)
