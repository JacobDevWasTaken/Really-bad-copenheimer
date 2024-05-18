import json

DISCOVER_CONFIG: dict
RESCAN_CONFIG: dict
INTERFACE_CONFIG: dict


def load_discover_config_file():
    global DISCOVER_CONFIG
    with open("config/discover.json", "r") as file:
        DISCOVER_CONFIG = json.load(file)


def load_rescan_config_file():
    global RESCAN_CONFIG
    with open("config/rescan.json", "r") as file:
        RESCAN_CONFIG = json.load(file)


def load_interface_config_file():
    global INTERFACE_CONFIG
    with open("config/interface.json", "r") as file:
        INTERFACE_CONFIG = json.load(file)


def load_config():
    load_discover_config_file()
    load_rescan_config_file()
    load_interface_config_file()


def load_value_from_key(obj: dict, key: str):
    keys = key.split(".")
    cob = obj.copy()
    try:
        for k in keys:
            cob = cob[k]
        return cob
    except Exception:
        return None


def load_discover_config(key):
    return load_value_from_key(DISCOVER_CONFIG, key)


def load_rescan_config(key):
    return load_value_from_key(RESCAN_CONFIG, key)


def load_interface_config(key):
    return load_value_from_key(INTERFACE_CONFIG, key)


load_config()
