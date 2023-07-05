"""
File: app.py
Description:Entry point of application.
Author: Ali G. Akyurek
Contact: aliakyurek@gmail.com
"""

from backend.device_manager import DeviceManager, InvalidDbError
from rich.table import Table
from rich import box
from rich.console import Console
from rich.panel import Panel
from tqdm import tqdm
import common
from common import print_error
import sys
import argparse
import logging

if __name__ == '__main__':
    # Create the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')

    # Parse the command-line arguments
    args = parser.parse_args()
    # Set up logging configuration
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

    # Create a logger
    logger = logging.getLogger(__name__)

    # Example usage of logging
    logger.debug('Running tool in debug mode')

    console = Console()
    console.print(Panel(f"Device Observer v{common.VERSION}", title="[green]Dev", subtitle="[red]Obs", expand=False))

    dm = DeviceManager()
    try:
        num_devices, num_attrs = dm.init_from_db("data/config.yml")

        if num_devices == 0:
            print("No devices registered\n")
        elif num_devices is not None:
            desc = f"{num_devices} devices registered. Enumerating..."
            progressor = tqdm(total=num_devices*num_attrs, ncols=75, desc=desc, leave=False,
                              bar_format="{desc} {percentage:3.0f}%|{bar}|")
            headers,rows = dm.dump_values(progressor)

            table = Table(show_lines=True, box=box.ASCII)
            for h in headers:
                table.add_column(h)
            table.columns[0].style = "cyan"
            for r in rows:
                r[-1] = ["[red]","[green]"][r[-1] == "OK"] + r[-1]
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