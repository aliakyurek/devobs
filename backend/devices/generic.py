"""
File: generic.py
Description:Support for generic device with IP.
Author: Ali G. Akyurek
Contact: aliakyurek@gmail.com
"""

from ..device import Device
from ..device import Attributes
import re
from ..comm import CommStage


class GenericIP(Device):
    __label__ = "Generic IP"
    __supports__ = "Any IP-based device"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)