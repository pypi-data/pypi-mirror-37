"""Utilities to read, write and manage the credentials file"""
from pathlib import Path
from getpass import getpass
import json
import stat
import os

CREDS = {}

CONFIG_DIR = Path.home()/'.swiftace'
CREDS_FILENAME = 'credentials.json'
CREDS_PATH = CONFIG_DIR/CREDS_FILENAME


def create_config_dir():
    CONFIG_DIR.mkdir(exist_ok=True)


def api_key_exists():
    """Check if API key is present in memory"""
    return 'API_KEY' in CREDS


def creds_file_exits():
    """Check if credentials file exits"""
    return CREDS_PATH.exists()


def read_creds_file():
    """Read the credentials file"""
    with open(str(CREDS_PATH), 'r') as f:
        return json.load(f)


def write_creds_file(creds):
    """Write the given credentials to file"""
    create_config_dir()
    os.system(f'touch {str(CREDS_PATH)}')
    with open(CREDS_PATH, 'w') as f:
        json.dump(creds, f)
    CREDS_PATH.chmod(stat.S_IREAD | stat.S_IWRITE)


def write_api_key(api_key, write_to_file=True):
    """Write the API key to memory, and the credentials file"""
    global CREDS
    CREDS['API_KEY'] = api_key
    if write_to_file:
        write_creds_file(CREDS)


def ask_api_key():
    """Ask the user to provide the API key"""
    print("[swiftace] Please enter your API key:")
    api_key = getpass()
    return api_key


def read_or_ask_api_key():
    """Read credentials file or ask the user for API Key"""
    if creds_file_exits():
        creds = read_creds_file()
        return creds['API_KEY'], False
    else:
        return ask_api_key(), True
