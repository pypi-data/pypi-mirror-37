"""Constants used throughout Farcy."""
import os
import re

__version__ = '1.3.0'

CONFIG_DIR = os.path.expanduser('~/.config/farcy')

MD_VERSION_STR = ('[farcy v{0}](https://github.com/appfolio/farcy)'
                  .format(__version__))

FARCY_COMMENT_START = '_{0}_'.format(MD_VERSION_STR)

NUMBER_RE = re.compile('(\d+)')

APPROVAL_PHRASES = [x.strip() for x in """
Amazing
Bravo
Excellent
Great job
Lookin' good
Outstanding work
Perfect
Spectacular
Tremendous
Well done
Wicked awesome
Winning
Wonderful
Wow
You are awesome
You do not miss a thing
""".split('\n') if x.strip()]

STATUS_CONTEXT = 'farcy'
