"""
File: device_manager.py
Description:Loading and enumerating devices.
Author: Ali G. Akyurek
Contact: aliakyurek@gmail.com
"""

from .device import Device, Attributes
from . import comm
import yaml
import time
from .devices import *
import logging
logger = logging.getLogger(__name__)
class InvalidDbError(Exception):
    pass

class DeviceManager:
    def __init__(self):
        self.devices = []

    def init_from_db(self, path):
        try:
            logger.debug("Opening configuration file")
            with open(path, 'r') as file:
                config = yaml.safe_load(file)

            logger.debug("Checking configuration file sanity")
            DeviceManager.check_db_sanity(config)

            if config["devices"] is None:
                config["devices"] = []
            for dev in config["devices"]:
                logger.debug(f"Creating device: {dev['label']}")
                comm_class_name = dev["comm"].pop("classname")
                comm_class = getattr(comm, comm_class_name)

                logger.debug(f"Instantiating comm. class: {comm_class_name}")
                comm_obj = comm_class(**dev["comm"])

                for device_class in Device.__subclasses__():
                    if device_class.__name__ == dev["classname"]:
                        logger.debug(f"Instantiating dev. class: {dev['classname']}")
                        device_obj = device_class(label=dev["label"], comm_interface=comm_obj)
                        self.devices.append(device_obj)
                        break
                else:
                    raise AttributeError(name=dev["classname"])
            logger.debug(f"Found {len(config['devices'])} with {len(Attributes.LIST)} attributes")
            result = len(config["devices"]), len(Attributes.LIST)

        except FileNotFoundError:
            # Handle the FileNotFoundError specifically
            raise InvalidDbError("Database file 'config.yml' not found under data folder")

        except InvalidDbError as e:
            # Handle the InvalidConfigError raised from check_db_sanity
            raise InvalidDbError(str(e))

        except AttributeError as e:
            raise InvalidDbError(f"Unimplemented class '{e.name}' referenced")

        except Exception as e:
            # Handle any other unexpected exceptions
            raise Exception("An error occurred during database initialization:", str(e))

        return result

    @staticmethod
    def check_db_sanity(config):
        if not isinstance(config, dict):
            raise InvalidDbError("Invalid config")

        if "db_ver" not in config or config["db_ver"] is None:
            raise InvalidDbError("Missing or invalid db version in 'db_ver' field")

        if "devices" not in config or (config["devices"] is not None and not isinstance(config["devices"], list)):
            raise InvalidDbError("Missing or invalid 'devices' field")

    def dump_values(self, progressor):
        headers = []
        rows = []

        for dev in self.devices:
            dev.begin()
            row = []
            for name, label in Attributes.LIST.items():
                if label not in headers:
                    headers.append(label)
                val = dev.get_attribute(name)
                row.append(val)
                progressor.update(1)
            rows.append(row)
            dev.end()
        progressor.close()
        return headers, rows
