"""
File: scalance_2nd_gen.py
Description:Support for 2nd generation (MSPS based) Siemens SCALANCE devices.
Author: Ali G. Akyurek
Contact: aliakyurek@gmail.com
"""

from backend.device import Device, Attributes
from backend.comm import CommStage
import re


class Scalance2ndGen(Device):
    __label__ = "SCALANCE 2nd Generation"
    __supports__ = "SCALANCE XR500, XM400, XB200, XP200, XC200, XR-300WG"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_attribute(Attributes.FIRMWARE_VERSION, CommStage.AUTH_OK, "show versions",
                           r"Firmware_Running\s+\|\s+(\S+)\s+\|")

        self.add_attribute(Attributes.DEV_TYPE,  CommStage.AUTH_OK, "show device information",
                           r"Device Type\s+\:\s+(.*)")

        self.add_attribute(Attributes.SYS_UPTIME,  CommStage.AUTH_OK, "show device information",
                           r"System Up Time\s+\:\s+(.*)")