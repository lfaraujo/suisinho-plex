import os
import discord
import yaml


def get_client():
    return discord.Client()


def get_client_id():
    with open("utils/config/dc_config.yml", "r") as f:
        config = yaml.safe_load(f.read())

    return config.get("client_id")


def is_empty(item_str):
    if item_str == "" or item_str == " " or "'- ****- ****'" in item_str or item_str is None:
        return True

    return False


def convert_to_list(list_to_add):
    if "&" not in list_to_add:
        return None

    list_to_add = list_to_add.split("& ")[1]

    if "," in list_to_add:
        return list_to_add.split(",")
    elif not is_empty(list_to_add):
        return list_to_add

    return None


def has_items(file):
    if os.stat(os.path.join(file)).st_size == 0:
        return False

    return True


def list_to_string(list_to_convert):
    if type(list_to_convert) == list and len(list_to_convert) > 1:
        return ', '.join(list_to_convert)
    elif type(list_to_convert) == list and len(list_to_convert) == 1:
        return list_to_convert[0]
    else:
        return list_to_convert


def exists(file, items):
    items_found = []

    if has_items(file):
        with open(file, "r", encoding="UTF-8") as gen_file:
            orig_data = gen_file.read().split(";")
            data_lower = [x.lower() for x in orig_data if not is_empty(x)]

            if type(items) == list:
                for item in items:
                    if item.strip().lower() in data_lower:
                        items_found.append(item.strip())

                if len(items_found) >= 1:
                    return True, list_to_string(items_found), orig_data
            elif items.strip().lower() in data_lower:
                return True, items, orig_data

    return False, ""
