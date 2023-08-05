# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

""" _common.py, A file for storing commonly-used functions."""
from __future__ import print_function

import json
import os
import sys

TOKEN_EXPIRE_TIME = 5 * 60
AZ_CLI_AAP_ID = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'
AML_WORKBENCH_CLI_CALLER = "AML_WORKBENCH_CLI_CALLER"

# EXTENSIONS AND FILE NAMES
RUNCONFIGURATION_EXTENSION = '.runconfig'
COMPUTECONTEXT_EXTENSION = '.compute'
TEAM_FILENAME = '.team'
ACCOUNT_FILENAME = 'runhistory'

# ARM RELATED CONSTANTS
ARM_ACCOUNT_DATA = "ARM_TEAM"
TEAM_LIST_OF_KEYS = {"subscriptions", "resourceGroups", "accounts", "workspaces"}
TEAM_DEFAULT_KEY = "id"
ACCOUNT_DEFAULT_KEY = "default"
CORRELATION_ID = None

# Environment variable names related to arm account token and user's email address.
# UX or any other service can set these environment variables in the python
# environment then the code uses values of these variables
AZUREML_ARM_ACCESS_TOKEN = "AZUREML_ARM_ACCESS_TOKEN"
AZUREML_USER_EMAIL_ID = "AZUREML_USER_EMAIL_ID"

# The subscription id environment variable. Mainly used for project commands.
AZUREML_SUBSCRIPTION_ID = "AZUREML_SUBSCRIPTION_ID"

# Environment variable for tenant id, mainly required for flighting.
AZUREML_TENANT_ID = "AZUREML_TENANT_ID"


# FILE LOCATIONS
if 'win32' in sys.platform:
    USER_PATH = os.path.expanduser('~')
    # TODO Rename CREDENTIALS_PATH since there aren't credentials there anymore.
    CREDENTIALS_PATH = os.path.join(USER_PATH, ".azureml")
    CIWORKBENCH_PATH = os.path.join(os.getenv('APPDATA'), 'ciworkbench', '.ci')
else:
    USER_PATH = os.path.join(os.getenv('HOME'), '.config')
    CREDENTIALS_PATH = os.path.join(os.getenv('HOME'), '.azureml')
    CIWORKBENCH_PATH = os.path.join(USER_PATH, 'ciworkbench', '.ci')


def normalize_windows_paths(path):
    """Convert windows paths to correct format"""
    if not path:
        return path
    if os.name == "nt":
        return path.replace("\\", "/")

    return path


def get_project_id(project):
    """Gets project id from metadata"""
    project = os.path.join(os.path.dirname(os.getcwd()), '.ci')

    with open(os.path.join(project, 'metadata'), 'r') as file:
        metadata = json.load(file)

    if 'Id' in metadata:
        return metadata['Id']
    else:
        raise ValueError('No project id found.')

# COMMAND RELATED METHODS


def create_common_argument(command_list, argument_name, argument_longcut,
                           argument_shortcut, argument_help):
    "Register common arguments for multiple commands"
    from azure.cli.core.commands import register_cli_argument
    for names in command_list:
        register_cli_argument(
            names,
            argument_name,
            options_list=(
                argument_longcut,
                argument_shortcut),
            help=argument_help)


def set_config_dir():
    """Get home directory"""
    if not os.path.exists(CREDENTIALS_PATH):
        os.makedirs(CREDENTIALS_PATH)

# RUNHISTORY FILE RELATED METHODS


def get_account_key():
    """Gets account key"""
    runhistory = os.path.join(CIWORKBENCH_PATH, ACCOUNT_FILENAME)

    with open(runhistory, 'r') as file:
        metadata = json.load(file)

    if 'AccountKey' in metadata:
        return metadata['AccountKey']
    else:
        raise ValueError('No account key found. Try creating an account/logging in.')


def get_development_url():
    """Gets development URL"""
    runhistory = os.path.join(CIWORKBENCH_PATH, ACCOUNT_FILENAME)

    with open(runhistory, 'r') as file:
        metadata = json.load(file)

    if 'RunHistoryEndpoint' in metadata:
        return metadata['RunHistoryEndpoint']
    else:
        raise ValueError('RunHistoryEndpoint not found. Try creating an account/logging in.')

# ARM RELATED METHODS


def check_for_keys(key_list, dictionary):
    """Checks if all keys are present in dictionary"""
    return True if all(k in dictionary for k in key_list) else False


def update_engine_account(account_id):
    """Tries to call Engine to update account information"""
    try:
        # Make Engine call, pass if cannot make it (means not calling from within Azure ML Workbench app)
        from vienna.Account import Account
        Account.create_account(account_id, ACCOUNT_DEFAULT_KEY)
    except ImportError:
        print("Command must be ran from within the application's shell for account information to be updated")
    except RuntimeError as e:
        print(e)
        os._exit(0)
