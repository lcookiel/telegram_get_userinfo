from telethon import TelegramClient, sync
from telethon import functions, types
from telethon.tl.types import InputPeerUser
import random


api_id = 1234567
api_hash = "1234567890abcdefghij123456789012"


client = TelegramClient("session", api_id, api_hash)
client.start()
# client.connect()


def importcontact(phone, first_name, last_name):
    result = client(functions.contacts.ImportContactsRequest(
            contacts=[types.InputPhoneContact(
                client_id=random.randrange(-2**63, 2**63),
                phone=phone,
                first_name=first_name,
                last_name=last_name
                )]
                ))
    entity = client.get_entity(phone)
    return entity.id, entity.access_hash, entity.phone, entity.username


def delete_contact(id, access_hash):
    result = client(functions.contacts.DeleteContactsRequest(
        [InputPeerUser(id, access_hash)]
        ))


def delete_messages(id, access_hash):
    messages = client.get_messages(InputPeerUser(id, access_hash), None)
    for message in messages:
        client.delete_messages(InputPeerUser(id, access_hash), message.id)


def get_userinfo(phone):
    try:
        id, access_hash, phone, username = importcontact(phone, "AAA", "")
    except ValueError:
        print("Phone number "+phone+" is not registered on Telegram.")
        id = None

    if id == None:
        return None
    else:
        client.send_message(InputPeerUser(id, access_hash), "hi")
        delete_messages(id, access_hash)
        delete_contact(id, access_hash)
        dialogs = client.get_dialogs()
        first_name = dialogs[0].entity.first_name
        last_name = dialogs[0].entity.last_name
        client.delete_dialog(InputPeerUser(id, access_hash), revoke=True)
        return id, phone, username, first_name, last_name


if __name__ == "__main__":
    if get_userinfo(phone) == None:
        pass
    else:
        id, phone, username, first_name, last_name = get_userinfo(phone)
        print([id, phone, username, first_name, last_name])
