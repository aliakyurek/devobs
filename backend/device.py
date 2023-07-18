"""
File: device.py
Description:Device abstraction and global attribute list.
Author: Ali G. Akyurek
Contact: aliakyurek@gmail.com
"""

from abc import ABC
import re
from .comm import *
import logging
logger = logging.getLogger(__name__)


class Attributes:
    STATE = "state"
    LABEL = "label"
    IP_ADDRESS = "ip_address"
    INTERFACE = "interface"
    FIRMWARE_VERSION = "firmware_version"
    SYS_UPTIME = "sys_uptime"
    DEV_TYPE = "device_type"
    WEBSERVER = "web_server"
    LIST = {
        LABEL: "Label",
        IP_ADDRESS: "IP Address",
        INTERFACE: "Interface",
        DEV_TYPE: "Device Type",
        FIRMWARE_VERSION: "Firmware Version",
        SYS_UPTIME: "System Up Time",
        WEBSERVER: "Web Server",
    }
Attributes.LIST[Attributes.STATE]="State"
class Device(ABC):
    # Existing code ...
    def __init__(self, label, comm_interface):
        self.comm_interface = comm_interface
        self.attributes = {}
        self.add_attribute(Attributes.STATE, CommStage.NOT_SET, self.get_access_state)
        self.add_attribute(Attributes.LABEL, CommStage.NOT_SET, lambda: label)
        self.add_attribute(Attributes.IP_ADDRESS, CommStage.NOT_SET, lambda: self.comm_interface.hostname)
        self.add_attribute(Attributes.INTERFACE, CommStage.NOT_SET, lambda: self.comm_interface.__label__)

    def add_attribute(self, name, min_stage, get_func, parse_func=None):
        """Adds device information to the device_info dictionary."""
        self.attributes[name] = {
            "min_stage": min_stage,
            "get_func": get_func,
            "parse_func": parse_func,
        }

    def get_attribute(self, name):
        """Retrieves device information for the specified attribute name."""
        response_ok = False
        for i in range(3):
            if response_ok == True:
                break
            response_ok = True
            response = "N/S"
            if name in self.attributes:
                response = "N/A"
                if self.comm_interface.stage >= self.attributes[name]["min_stage"]:
                    attr = self.attributes[name]
                    command_or_func = attr.get("get_func")
                    parser_pattern_or_func = attr.get("parse_func", None)
                    if isinstance(command_or_func, str):
                        response = self.comm_interface.execute_request(command_or_func)
                    elif callable(command_or_func):
                        response = command_or_func()
                    if parser_pattern_or_func:
                        if isinstance(parser_pattern_or_func, str):
                            compiled_pattern = re.compile(parser_pattern_or_func, re.MULTILINE)
                            match = compiled_pattern.search(response)
                            if match:
                                response = match.group(1)
                            else:
                                response_ok = False
                                logger.debug(f"Unexpected response: {response}")
                        elif callable(parser_pattern_or_func):
                            response = parser_pattern_or_func(response)
        return response.split('\n')[0]

    def get_access_state(self):
        s = self.comm_interface.stage
        r = ""
        if s == CommStage.AUTH_OK or s == CommStage.IP_OK:
            r = "OK"
        elif s == CommStage.AUTH_TRY:
            r = "Auth. failed"
        elif s == CommStage.PROT_TRY:
            r = "Protocol failed"
        elif s == CommStage.IP_TRY:
            r = "Ping failed"
        return r

    def get_prompt(self):
        if isinstance(self.comm_interface, SSHCommInterface):
            return self.comm_interface.prompt
        return ""

    def begin(self):
        self.comm_interface.establish()

    def end(self):
        self.comm_interface.teardown()
