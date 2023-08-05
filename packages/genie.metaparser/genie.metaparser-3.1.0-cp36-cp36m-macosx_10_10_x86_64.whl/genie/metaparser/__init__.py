__version__ = '3.1.0'
__author__ = 'Cisco Systems Inc.'
__contact__ = ['pyats-support@cisco.com', 'pyats-support-ext@cisco.com']
__copyright__ = 'Copyright (c) 2018, Cisco Systems Inc.'

import re
from ._metaparser import *

_IMPORTMAP = {
    re.compile(r'^metaparser(?=$|\.)'): 'genie.metaparser'
}
