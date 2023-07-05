"""
File: scalance_3rd_gen.py
Description:Support for 3rd generation (SinecOS based) Siemens SCALANCE devices.
Author: Ali G. Akyurek
Contact: aliakyurek@gmail.com
"""

from backend.device import Device, Attributes
from backend.comm import CommStage
import re


class Scalance3rdGen(Device):
    __label__ = "SCALANCE 3rd Generation"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_attribute(Attributes.DEV_TYPE, CommStage.AUTH_OK, 'show system hardware | until chassis',
                           r"^(.+)\s+chassis\s+Family")
        self.add_attribute(Attributes.FIRMWARE_VERSION, CommStage.AUTH_OK,
                           'show system firmware | until "Running SINEC OS Firmware"',
                           r"^Running SINEC OS Firmware\s+(\S+)\.00")



        self.add_attribute(Attributes.SYS_UPTIME,  CommStage.AUTH_OK, "show system state",
                           Scalance3rdGen.parse_sys_uptime)

    @staticmethod
    def parse_sys_uptime(response):
        val = "N/A"
        compiled_pattern = re.compile("^state uptime\s+(\S+)",re.MULTILINE)

        # Use regex to find the firmware version
        match = compiled_pattern.search(response)
        if match:
            val = match.group(1)
            parts = []
            buf = ""
            for c in val:
                buf += c
                if c.isalpha():
                    parts.append(buf)
                    buf = ""
            val = " ".join(parts)
        return val

if __name__ == '__main__':
    print(Scalance3rdGen.parse_sys_uptime("state uptime 12d3h30m20s"))
