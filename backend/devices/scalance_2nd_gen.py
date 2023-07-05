"""
File: scalance_2nd_gen.py
Description:Support for 2nd generation (MSPS based) Siemens SCALANCE devices.
Author: Ali G. Akyurek
Contact: ali.akyurek@siemens.com
"""

from backend.device import Device, Attributes
from backend.comm import CommStage
import re


class Scalance2ndGen(Device):
    __label__ = "SCALANCE 2nd Generation"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_attribute(Attributes.FIRMWARE_VERSION, CommStage.AUTH_OK, "show versions",
                           r"Firmware_Running\s+\|\s+(\S+).00\S+\s+\|")

        self.add_attribute(Attributes.DEV_TYPE,  CommStage.AUTH_OK, "show device information",
                           r"Device Type\s+\:\s+(.*)")

        self.add_attribute(Attributes.SYS_UPTIME,  CommStage.AUTH_OK, "show device information",
                           r"System Up Time\s+\:\s+(.*)")