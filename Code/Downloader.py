"""Ensure required Modules are installed"""
"""The code on this page is based on the following Stack Overflow post:
Stack Overflow. 2010. "Check if Module Exists, If Not Install It." December 23, 2010.
https://stackoverflow.com/questions/4527554/check-if-module-exists-if-not-install-it."""

def install_if_missing(package):
    import importlib
    import subprocess
    import sys

    try:
        importlib.import_module(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
