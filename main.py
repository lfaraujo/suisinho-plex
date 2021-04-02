from utils.main import *
from plex.main import *

client = get_client()
logger = get_logger()
token = get_access_token(get_plex_auth())


@client.event
async def on_ready():
    logger.info("step=connectDiscord user={0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_content = message.content

    logger.info("step=receiveMessage author=%s, content=%s" % (message.author.name, message_content))

    if message_content.startswith("-hello"):
        await message.channel.send(get_message("greetings") % message.author.name + get_emoticon("smile_cat"))
        await message.channel.send(list_obj_to_list_str(get_commands()))
        await message.channel.send(get_message("usage_tips"))
        await message.channel.send(get_message("multiple_items"))

    if message_content.startswith("-movies-list"):
        await message.channel.send(get_list("movies"))

    if message_content.startswith("-series-list"):
        await message.channel.send(get_list("series"))

    if message_content.startswith("-animes-list"):
        await message.channel.send(get_list("animes"))

    if message_content.startswith("-add-movies"):
        await message.channel.send(add_items(convert_to_list(message_content), "movies"))

    if message_content.startswith("-add-series"):
        await message.channel.send(add_items(convert_to_list(message_content), "series"))

    if message_content.startswith("-add-animes"):
        await message.channel.send(add_items(convert_to_list(message_content), "animes"))

    if message_content.startswith("-remove-movies"):
        await message.channel.send(remove_item(convert_to_list(message_content), "movies"))

    if message_content.startswith("-remove-series"):
        await message.channel.send(remove_item(convert_to_list(message_content), "series"))

    if message_content.startswith("-remove-animes"):
        await message.channel.send(remove_item(convert_to_list(message_content), "animes"))

    if message_content.startswith("-avaiable-libraries"):
        await message.channel.send(list_obj_to_list_str(get_libraries(token)))


def add_items(items, item_type):
    if items is None:
        return get_message("invalid_format_error") + get_emoticon("pouting_cat")

    logger.info("step=add_items items=%s item_type=%s" % (items, item_type))

    path = get_path(item_type)

    is_duplicate = exists(path, items)

    with open(path, "a+", encoding="UTF-8") as gen_list:
        if type(items) == list:
            for item in items:
                if not is_duplicate[0]:
                    gen_list.write(item.strip() + ";")
        elif not is_duplicate[0]:
            gen_list.write(items.strip() + ";")

        if is_duplicate[0]:
            logger.warning("step=add_items_duplicate dupe_items=%s" % is_duplicate[1])
            return get_message("duplicate_items") % is_duplicate[1] + get_emoticon("kissing_cat")

        return get_message("add_success") + get_emoticon("kissing_cat")


def remove_item(item, item_type):
    if item is None or type(item) == list:
        return get_message("invalid_format_error") + get_emoticon("pouting_cat")

    logger.info("step=remove_item item=%s item_type=%s" % (item, item_type))

    path = get_path(item_type)
    check_result = exists(path, item)

    if check_result[0]:
        with open(path, "w", encoding="UTF-8") as gen_list:
            for data in check_result[2]:
                if not is_empty(data) and data.lower() != item.strip().lower():
                    gen_list.write(data.strip() + ";")

    return get_message("remove_success") + get_emoticon("smile_cat")


def get_list(item_type):
    message = ""

    with open(get_path(item_type), "r", encoding="UTF-8") as gen_list:
        list_items = [x for x in gen_list.read().split(";") if not is_empty(x)]

        for item in list_items:
            if is_empty(message):
                message += "- **%s**" % item
            else:
                message += "\n- **%s**" % item

    if is_empty(message):
        message = get_message("empty_list") + get_emoticon("crying_cat")

    return message


if __name__ == "__main__":
    client.run(get_client_id())
