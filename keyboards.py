from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class IsIdPrepayment(CallbackData, prefix='id', sep=':'):
    payment_id: str


class Pay(CallbackData, prefix='pay', sep=':'):
    pay_id: str


def keyboard_prepayment(url:str, id_payment):
    kb = InlineKeyboardBuilder()
    kb.row(*[InlineKeyboardButton(text='Оплатить 💳', url=url),
             InlineKeyboardButton(text='Проверка оплаты ✅',
                                  callback_data=Pay(pay_id=id_payment).pack())],
           width=1)
    return kb.as_markup()
