from telethon.sync import TelegramClient
from telegram.config import api_id, api_hash
from loguru import logger


client = TelegramClient('sms', api_id, api_hash)
client.start()


def send_message(phone, message):
    try:
        contact = client.get_entity(str(phone))
        client.send_message(entity=contact, message=str(message))
        return True
    except Exception as e:
        logger.error('Не могу найти контакт')
        return False
