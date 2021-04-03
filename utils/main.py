import os
import discord
import yaml
from logging import config, getLogger


def get_client():
    return discord.Client()


def get_client_id():
    return os.environ["dc_client_id"]


def get_plex_auth():
    return os.environ["plex_user"], os.environ["plex_password"]


def get_server_address():
    return os.environ["plex_server_address"]


def get_logger():
    with open("config/log_config.yml", "r") as f:
        log_config = yaml.safe_load(f.read())
        config.dictConfig(log_config)

    return getLogger('main_app')


def get_path(item_type):
    with open("config/path_list.yml", "r") as f:
        path_list = yaml.safe_load(f.read())
        return path_list.get(item_type)


def get_emoticon(emoticon):
    with open("config/messages.yml", "r") as f:
        messages_file = yaml.safe_load(f.read())
        emoticons = messages_file.get("emoticons")

        return emoticons.get(emoticon)


def get_message(message):
    with open("config/messages.yml", "r", encoding="UTF-8") as f:
        messages_file = yaml.safe_load(f.read())
        messages = messages_file.get("messages")

        return messages.get(message)


def get_commands():
    with open("config/messages.yml", "r", encoding="UTF-8") as f:
        messages_file = yaml.safe_load(f.read())
        commands = messages_file.get("commands")

        commands_list = [commands.get(x) for x in commands]

        return commands_list


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


def list_obj_to_list_str(list_to_convert):
    list_str = ""

    for item in list_to_convert:
        if "`" not in item:
            list_str += "\n- `%s`" % item
        else:
            list_str += "\n%s" % item

    return list_str


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
