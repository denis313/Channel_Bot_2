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


def create_payment(amount: int, description: str, chat_id: int, name, phone):
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
        "receipt": {
            "customer": {
                "full_name": name,
                "email": "email@email.ru",
                "phone": "79211234567"
            },
            "items": [
                {
                    "description": "плата подписки",
                    "quantity": "1.00",
                    "amount": {
                        "value": amount,
                        "currency": "RUB"
                    },
                    "vat_code": "2",
                    "payment_mode": "full_payment",
                    "payment_subject": "commodity",
                    "country_of_origin_code": "CN",
                    "product_code": "44 4D 01 00 21 FA 41 00 23 05 41 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 AB 00",
                    "customs_declaration_number": "10714040/140917/0090376",
                    "excise": "20.00",
                    "supplier": {
                        "name": "string",
                        "phone": "string",
                        "inn": "string"
                    }
                },
            ]
        },
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

l ={"receipt": {
            "customer": {
                "full_name": "Ivanov Ivan Ivanovich",
                "email": "email@email.ru",
                "phone": "79211234567",
                "inn": "6321341814"
            },
            "items": [
                {
                    "description": "Переносное зарядное устройство Хувей",
                    "quantity": "1.00",
                    "amount": {
                        "value": 1000,
                        "currency": "RUB"
                    },
                    "vat_code": "2",
                    "payment_mode": "full_payment",
                    "payment_subject": "commodity",
                    "country_of_origin_code": "CN",
                    "product_code": "44 4D 01 00 21 FA 41 00 23 05 41 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 AB 00",
                    "customs_declaration_number": "10714040/140917/0090376",
                    "excise": "20.00",
                    "supplier": {
                        "name": "string",
                        "phone": "string",
                        "inn": "string"
                    }
                },
            ]
        }
    }
