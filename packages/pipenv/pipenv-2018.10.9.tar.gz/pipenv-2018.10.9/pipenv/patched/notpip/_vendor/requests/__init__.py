# -*- coding: utf-8 -*-

#   __
#  /__)  _  _     _   _ _/   _
# / (   (- (/ (/ (- _)  /  _)
#          /

"""
Requests HTTP Library
~~~~~~~~~~~~~~~~~~~~~

Requests is an HTTP library, written in Python, for human beings. Basic GET
usage:

   >>> import requests
   >>> r = requests.get('https://www.python.org')
   >>> r.status_code
   200
   >>> 'Python is a programming language' in r.content
   True

... or POST:

   >>> payload = dict(key1='value1', key2='value2')
   >>> r = requests.post('http://httpbin.org/post', data=payload)
   >>> print(r.text)
   {
     ...
     "form": {
       "key2": "value2",
       "key1": "value1"
     },
     ...
   }

The other HTTP methods are supported - see `requests.api`. Full documentation
is at <http://python-requests.org>.

:copyright: (c) 2017 by Kenneth Reitz.
:license: Apache 2.0, see LICENSE for more details.
"""

from pipenv.patched.notpip._vendor import urllib3
from pipenv.patched.notpip._vendor import chardet
import warnings
from .exceptions import RequestsDependencyWarning


def check_compatibility(urllib3_version, chardet_version):
    urllib3_version = urllib3_version.split('.')
    assert urllib3_version != ['dev']  # Verify urllib3 isn't installed from git.

    # Sometimes, urllib3 only reports its version as 16.1.
    if len(urllib3_version) == 2:
        urllib3_version.append('0')

    # Check urllib3 for compatibility.
    major, minor, patch = urllib3_version  # noqa: F811
    major, minor, patch = int(major), int(minor), int(patch)
    # urllib3 >= 1.21.1, <= 1.23
    assert major == 1
    assert minor >= 21
    assert minor <= 23

    # Check chardet for compatibility.
    major, minor, patch = chardet_version.split('.')[:3]
    major, minor, patch = int(major), int(minor), int(patch)
    # chardet >= 3.0.2, < 3.1.0
    assert major == 3
    assert minor < 1
    assert patch >= 2


def _check_cryptography(cryptography_version):
    # cryptography < 1.3.4
    try:
        cryptography_version = list(map(int, cryptography_version.split('.')))
    except ValueError:
        return

    if cryptography_version < [1, 3, 4]:
        warning = 'Old version of cryptography ({0}) may cause slowdown.'.format(cryptography_version)
        warnings.warn(warning, RequestsDependencyWarning)

# Check imported dependencies for compatibility.
try:
    check_compatibility(urllib3.__version__, chardet.__version__)
except (AssertionError, ValueError):
    warnings.warn("urllib3 ({0}) or chardet ({1}) doesn't match a supported "
                  "version!".format(urllib3.__version__, chardet.__version__),
                  RequestsDependencyWarning)

# Attempt to enable urllib3's SNI support, if possible
from pipenv.patched.notpip._internal.compat import WINDOWS
if not WINDOWS:
    try:
        from pipenv.patched.notpip._vendor.urllib3.contrib import pyopenssl
        pyopenssl.inject_into_urllib3()

        # Check cryptography version
        from cryptography import __version__ as cryptography_version
        _check_cryptography(cryptography_version)
    except ImportError:
        pass

# urllib3's DependencyWarnings should be silenced.
from pipenv.patched.notpip._vendor.urllib3.exceptions import DependencyWarning
warnings.simplefilter('ignore', DependencyWarning)

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __build__, __author__, __author_email__, __license__
from .__version__ import __copyright__, __cake__

from . import utils
from . import packages
from .models import Request, Response, PreparedRequest
from .api import request, get, head, post, patch, put, delete, options
from .sessions import session, Session
from .status_codes import codes
from .exceptions import (
    RequestException, Timeout, URLRequired,
    TooManyRedirects, HTTPError, ConnectionError,
    FileModeWarning, ConnectTimeout, ReadTimeout
)

# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

# FileModeWarnings go off per the default.
warnings.simplefilter('default', FileModeWarning, append=True)
