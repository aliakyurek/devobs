"""
File: __init__.py
Description:Entry point of devices module.
Author: Ali G. Akyurek
Contact: ali.akyurek@siemens.com
"""

import pkgutil

# Get the current package name
package_name = __name__

# Iterate over all submodules in the current package
for _, module_name, _ in pkgutil.walk_packages(path=__path__, prefix=package_name + '.'):
    # Import the module
    __import__(module_name)