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
        self.add_attribute(Attributes.DEV_TYPE,  CommStage.AUTH_OK, "show device information",
                           r"Device Type\s+\:\s+(.*)")

        self.add_attribute(Attributes.FIRMWARE_VERSION, CommStage.AUTH_OK, "show versions",
                           r"Firmware_Running\s+\|\s+(\S+)\s+\|")

        self.add_attribute(Attributes.SYS_UPTIME,  CommStage.AUTH_OK, "show device information",
                           r"System Up Time\s+\:\s+(.*)")

        self.add_attribute(Attributes.WEBSERVER,  CommStage.AUTH_OK, self.get_webserver_status, None)

    def get_webserver_status(self):
        webservers = []
        response = self.comm_interface.execute_request("show ip http server status")
        match = re.search(r"HTTP server status\s+: (\S+)", response, re.MULTILINE)
        state = match.group(1) if match else ""
        if state == "Enabled":
            if match := re.search(r"HTTP port is\s+: (\S+)", response, re.MULTILINE):
                webservers.append(f"HTTP({match.group(1)})")

        response = self.comm_interface.execute_request("show ip http secure server status")
        match = re.search(r"HTTP secure server status\s+: (\S+) \(", response, re.MULTILINE)
        state = match.group(1) if match else ""
        if state == "Enabled":
            if match := re.search(r"Port\s+: (\S+)", response, re.MULTILINE):
                webservers.append(f"HTTPS({match.group(1)})")
        return ",".join(webservers)