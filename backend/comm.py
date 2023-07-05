"""
File: comm.py
Description:Abstract and concrete communication classes
Author: Ali G. Akyurek
Contact: aliakyurek@gmail.com
"""

from abc import ABC, abstractmethod
import ping3
import paramiko
import time
from paramiko.ssh_exception import *
import logging
logger = logging.getLogger(__name__)
logging.getLogger('paramiko').setLevel(logging.CRITICAL + 1)

class CommStage:
    NOT_SET = 0
    IP_TRY = 1
    IP_OK = 2
    PROT_TRY = 3
    PROT_OK = 4
    AUTH_TRY = 5
    AUTH_OK = 6


class CommInterface(ABC):
    def __init__(self):
        self.stage = CommStage.NOT_SET

    @abstractmethod
    def establish(self):
        """Abstract method to establish communication."""
        pass

    def execute_request(self, request):
        """Abstract method to execute a request."""
        pass

    def teardown(self):
        """Abstract method to teardown communication."""
        pass


class IPCommInterface(CommInterface):
    __label__ = "IP"

    def __init__(self, hostname):
        super().__init__()
        self.hostname = hostname

    def establish(self):
        logger.debug(f"Establishing IP communication to {self.hostname}")
        self.stage = CommStage.IP_TRY
        res = ping3.ping(self.hostname)
        if not (res is False or res is None):
            self.stage = CommStage.IP_OK
        logger.debug(f"IP communication to {self.hostname} is {('FAIL', 'OK')[self.stage == CommStage.IP_OK] }")

class TCPCommInterface(IPCommInterface):
    __label__ = "TCP"

    def __init__(self, port, **kwargs):
        super().__init__(**kwargs)
        self.port = port

    def establish(self):
        super().establish()
class SSHCommInterface(TCPCommInterface):
    __label__ = "SSH"

    def __init__(self, username, password, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.password = password
        self.client = None
        self.shell = None

    def establish(self):
        super().establish()
        if self.stage != CommStage.IP_OK:
            return

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            logger.debug(f"Establishing SSH communication to {self.hostname}")
            self.client.connect(self.hostname, self.port, self.username, self.password, timeout=3)
            logger.debug(f"SSH communication to {self.hostname} is OK")
            logger.debug(f"Invoking shell")
            self.shell = self.client.invoke_shell()
            logger.debug(f"SSH shell acquired")
        except AuthenticationException:
            self.stage = CommStage.AUTH_TRY
        except (SSHException, NoValidConnectionsError, TimeoutError):
            self.stage = CommStage.PROT_TRY
        except Exception as e:
            self.stage = CommStage.PROT_TRY
        else:
            self.stage = CommStage.PROT_OK
            self.stage = CommStage.AUTH_OK

    def execute_request(self, command):
        """Implement SSH command execution logic here."""
        # SSH command execution code
        logger.debug(f"Sending command via SSH: {command}")
        self.shell.send(f'{command}\n')
        time.sleep(1)
        # Receive and print the output of the commands
        output = ''
        while True:
            if self.shell.recv_ready():
                output += self.shell.recv(32).decode().replace('\r', '')
            else:
                break
        logger.debug(f"Response: {output}")
        return output

    def teardown(self):
        if self.client:
            self.client.close()