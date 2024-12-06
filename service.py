import re
import uuid

from aiogram.types import Message, CallbackQuery

from aiogram.types import FSInputFile
from aiogram.filters import BaseFilter
from bot import bot
from config import db_config, yookassa
from database.requests import DatabaseManager
from yookassa import Configuration, Payment

from lexicon import lexicon


def create_payment(amount: int, description: str, chat_id: int):
    account_id, secret_key = yookassa()
    Configuration.account_id = account_id
    Configuration.secret_key = secret_key
    payment = Payment.create({
        "amount": {
            "value": f"{amount}.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/sharmoscow_bot"
        },
        "payment_method_data": {
            "type": "sbp"
        },
        "capture": True,
        "metadata": {
            'chat_id': chat_id
        },
        "description": description
    }, uuid.uuid4())
    print(payment)
    return payment.confirmation.confirmation_url, payment.id


def get_photo():
    photo = FSInputFile('img.png', filename=f'photo_img')
    return photo
