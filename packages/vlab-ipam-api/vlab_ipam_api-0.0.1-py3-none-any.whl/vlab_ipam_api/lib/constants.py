# -*- coding: UTF-8 -*-
"""
All the things can override via Environment variables are keep in this one file.

.. note::
    Any and all values that *are* passwords must contain the string 'AUTH' in
    the name of the constant. This is how we avoid logging passwords.
"""
from os import environ
import socket
from collections import namedtuple, OrderedDict


DEFINED = OrderedDict([
            ('VLAB_IPAM_LOG_LEVEL', environ.get('VLAB_IPAM_LOG_LEVEL', 'INFO')),
            ('VLAB_URL', environ.get('VLAB_URL', 'https://localhost')),
            # Only the owner of the firewall can make changes - see views for context
            ('VLAB_IPAM_OWNER', socket.gethostname().split('.')[0]),
          ])

Constants = namedtuple('Constants', list(DEFINED.keys()))

# The '*' expands the list, just liked passing a function *args
const = Constants(*list(DEFINED.values()))
