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
    __supports__ = "SCALANCE XCM300, XRM300"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_attribute(Attributes.DEV_TYPE, CommStage.AUTH_OK, 'show system hardware | until chassis',
                           r"^(.+)\s+chassis\s+Family")

        self.add_attribute(Attributes.FIRMWARE_VERSION, CommStage.AUTH_OK,
                           'show system firmware | until "Running SINEC OS Firmware"',
                           r"^Running SINEC OS Firmware\s+(\S+)")

        self.add_attribute(Attributes.SYS_UPTIME,  CommStage.AUTH_OK, "show system state",
                           self.parse_sys_uptime)

        self.add_attribute(Attributes.WEBSERVER,  CommStage.AUTH_OK, self.get_webserver_status,
                           None)

    @staticmethod
    def parse_sys_uptime(response):
        val = "N/A"
        compiled_pattern = re.compile(r"^state uptime\s+(\S+)", re.MULTILINE)

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

    def get_webserver_status(self):
        webservers = []
        response = self.comm_interface.execute_request("show running-config system management-services webui \
        | details | until tls")
        match = re.search(r"endpoint unsecure$\s+(.+)$", response, re.MULTILINE)
        state = match.group(1) if match else ""
        if state == "enabled":
            if match := re.search(r"http$\s+tcp$\s+port (\S+)", response, re.MULTILINE):
                webservers.append(f"HTTP({match.group(1)})")

        match = re.search(r"endpoint secure$\s+(.+)$", response, re.MULTILINE)
        state = match.group(1) if match else ""
        if state == "enabled":
            if match := re.search(r"https$\s+tcp$\s+port (\S+)", response, re.MULTILINE):
                webservers.append(f"HTTPS({match.group(1)})")
        return ",".join(webservers)


if __name__ == '__main__':
    print(Scalance3rdGen.parse_sys_uptime("state uptime 12d3h30m20s"))
