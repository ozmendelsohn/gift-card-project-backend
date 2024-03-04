import os
import pathlib
import yaml
import json

"""
Expecting the following strcture:
- config
- src
|-- utils.py (current file)
"""
# Get the absolute path of the current file
MAIN_DIR = pathlib.Path(__file__).resolve().parent.parent
CONFIG_DIR = os.path.join(MAIN_DIR, 'config')
SECRETS_FILE = os.path.join(MAIN_DIR, 'secrets.json')

def replace_secrets(config: dict, secrets: dict, preset:str = "SECRET__") -> dict:
    """
    Replace the keys in the config file with the values from the secrets file.

    Parameters
    ----------
    config : dict
        The configuration dictionary.
    secrets : dict
        The secrets dictionary.
    preset : str, optional
        The preset for the secrets keys (default is "SECRET__").

    Returns
    -------
    dict
        The configuration dictionary with the replaced keys.
    """
    for key, value in list(config.items()):
        if isinstance(value, dict):
            config[key] = replace_secrets(value, secrets, preset)
        else:
            if key.startswith(preset):
                # remove the preset from the key
                new_key = key[len(preset):]
                config[new_key] = secrets[value]
                # remove the old key
                config.pop(key)
    return config

def load_config(config: str,
                config_path: str = CONFIG_DIR,
                secrets_file: str = SECRETS_FILE,
                file_format: str = 'yaml') -> dict:
    """
    Load a configuration file.

    Parameters
    ----------
    config : str
        The path to the configuration file.
    config_path : str, optional
        The name of the configuration file (default is CONFIG_DIR).
    secrets_file : str, optional
        The name of the secrets file (default is SECRETS_FILE).
    file_format : str, optional
        The format of the configuration file (default is 'yaml').

    Returns
    -------
    dict
        A dictionary containing the loaded configuration.
    """
    # check if the path and the file exist

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config folder not found: {config_path}")
    if not os.path.exists(os.path.join(config_path, config)):
        raise FileNotFoundError(f"Config file not found: {config}")
    
    # load the configuration file
    with open(os.path.join(config_path, config), 'r') as file:
        if file_format == 'yaml':
            config_dict = yaml.safe_load(file)
        elif file_format == 'json':
            config_dict = json.load(file)
        else:
            raise ValueError(f"File format not supported: {file_format}")
        
    # replace key with "SECRETS__" with the value from the secrets file including recursive keys
    if os.path.exists(secrets_file):
        with open(secrets_file, 'r') as file:
            secrets = json.load(file)
        config_dict = replace_secrets(config_dict, secrets)
    else:
        FileNotFoundError(f"Secrets file not found: {secrets_file}")

    return config_dict
