"""
File: app.py
Description:Entry point of application.
Author: Ali G. Akyurek
Contact: aliakyurek@gmail.com
"""

import logging
import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose mode')
group.add_argument('-l', '--list', action='store_true', help='list supported devices')
group.add_argument('-d', '--daemon', action='store_true', help='start websocket daemon')

# Parse the command-line arguments
args = parser.parse_args()
# Set up logging configuration
logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

from backend.device_manager import DeviceManager, InvalidDbError
from frontend import wserver
from rich.table import Table
from rich import box
from rich.console import Console
from rich.panel import Panel
from tqdm import tqdm
import common

import sqlite3

def show_devices():
    dm = DeviceManager.get_instance()
    try:
        num_devices, num_attrs = dm.init_from_db("data/config.yml")

        if num_devices == 0:
            print("No devices registered\n")
        elif num_devices is not None:
            desc = f"{num_devices} devices registered. Enumerating..."
            progressor = tqdm(total=num_devices*num_attrs, ncols=75, desc=desc, leave=False,
                              bar_format="{desc} {percentage:3.0f}%|{bar}|")
            df = dm.tabularize_devices(progressor).copy()

            table = Table(show_lines=True, box=box.ASCII)
            for h in df.columns:
                table.add_column(h)
            table.columns[0].style = "cyan"
            df['State'] = df['State'].apply(lambda x: '[green]' + x if x == 'OK' else '[red]' + x)

            for _, r in df.iterrows():
                table.add_row(*r)

            console.print(table)
            print("N/A: Not available")
            print("N/S: Not supported")

    except InvalidDbError as e:
        # Handle the InvalidDbError and display the error message
        print("Database error:", str(e))

    except Exception as e:
        # Handle any other unexpected exceptions
        print("An error occurred:", str(e))
    print("")

def show_supported_devices():
    dm = DeviceManager.get_instance()
    dm.init_devicemap()
    headers, rows = dm.tabularize_devicemap()

    table = Table(show_lines=True, box=box.ASCII)
    for h in headers:
        table.add_column(h)
    table.columns[0].style = "cyan"
    for r in rows:
        table.add_row(*r)

    console.print(table)

if __name__ == '__main__':
    # Create the argument parser
    # Create a logger
    logger = logging.getLogger(__name__)

    # Example usage of logging
    logger.debug('Running tool in debug mode')

    console = Console()
    console.print(Panel(f"Device Observer {common.VERSION}", title="[green]Dev", subtitle="[red]Obs", expand=False))

    if args.list:
        show_supported_devices()
    else:
        show_devices()

    if args.daemon:
        wserver.main()

