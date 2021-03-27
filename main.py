from utils.main import *
from logger.main import *

client = get_client()
logger = get_logger()

smile_cat = ":smile_cat:"
pouting_cat = ":pouting_cat:"
kissing_cat = ":kissing_cat:"
crying_cat = ":crying_cat_face:"

add_success_msg = "Item(ns) adicionado(s)! **PURR** %s" % kissing_cat
remove_success_msg = "O item foi removido com sucesso! **PURR** %s" % smile_cat
invalid_format_error = "O formato do(s) item(ns) enviado(s) é inválido! **MEOW** %s" % pouting_cat
multiple_items_msg = "Caso queira enviar mais de 1 item, utilize `,` para separar os itens."
single_item_msg = "Apenas um item deve ser enviado por vez."
empty_list_msg = "Ainda não há itens nesta lista! %s" % crying_cat

path_list = {"movies": "data/lista_filmes.txt", "series": "data/lista_series.txt", "animes": "data/lista_animes.txt"}

commands = {"-movies-list": "Lista de filmes a serem adicionados",
            "-series-list": "Lista de séries a serem adicionadas",
            "-animes-list": "Lista de animes a serem adicionados",
            "-add-movies": "Adiciona filmes à lista. %s" % multiple_items_msg,
            "-add-series": "Adiciona series à lista. %s" % multiple_items_msg,
            "-add-animes": "Adiciona animes à lista. %s" % multiple_items_msg,
            "-remove-movies": "Remove filmes da lista.  %s" % single_item_msg,
            "-remove-series": "Remove series da lista. %s" % single_item_msg,
            "-remove-animes": "Remove animes da lista. %s" % single_item_msg,
            }


@client.event
async def on_ready():
    logger.info("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_content = message.content

    logger.info("step=receiveMessage author=%s, content=%s" % (message.author.name, message_content))

    if message_content.startswith("-hello"):
        await message.channel.send("Olá, %s! Segura a lista de comandos! Adicione sempre `&` após o comando! **MEOW** "
                                   "%s" % (message.author.name, smile_cat))
        await message.channel.send(mount_commands())

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


def mount_commands():
    message = ""

    for command in commands:
        message += "\n`%s` - %s" % (command, commands[command])

    return message


def add_items(items, item_type):
    if items is None:
        return invalid_format_error

    logger.info("step=add_items items=%s item_type=%s" % (items, item_type))

    path = path_list[item_type]

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
            return "O(s) item(ns) **%s** já está(ão) na lista e não foi(ram) adicionado(s)! Os demais foram " \
                   "adicionados com sucesso! **PURR** %s" % (is_duplicate[1], kissing_cat)

        return add_success_msg


def remove_item(item, item_type):
    if item is None or type(item) == list:
        return invalid_format_error

    logger.info("step=remove_item item=%s item_type=%s" % (item, item_type))

    path = path_list[item_type]
    check_result = exists(path, item)

    if check_result[0]:
        with open(path, "w", encoding="UTF-8") as gen_list:
            for data in check_result[2]:
                if not is_empty(data) and data.lower() != item.strip().lower():
                    gen_list.write(data.strip() + ";")

    return remove_success_msg


def get_list(item_type):
    message = ""

    with open(path_list[item_type], "r", encoding="UTF-8") as gen_list:
        list_items = [x for x in gen_list.read().split(";") if not is_empty(x)]

        for item in list_items:
            if is_empty(message):
                message += "- **%s**" % item
            else:
                message += "\n- **%s**" % item

    if is_empty(message):
        message = empty_list_msg

    return message


if __name__ == "__main__":
    client.run(get_client_id())