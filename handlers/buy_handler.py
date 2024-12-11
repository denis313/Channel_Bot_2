import logging
import json
from datetime import timedelta, date

import yookassa
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, InputMediaPhoto

from config import admin_id, db_config
from database.requests import DatabaseManager
from keyboards import Pay, IsIdPrepayment
from lexicon import lexicon
from service import create_payment, get_photo

logger = logging.getLogger(__name__)
router = Router()
dsn = db_config()
db_manager = DatabaseManager(dsn=dsn)


@router.callback_query(Pay.filter())
async def successful_payment_handler(callback: CallbackQuery, bot: Bot, callback_data: Pay):
    start_date = date.today()
    end_date = start_date + timedelta(days=30)
    user = await db_manager.get_user(user_id=callback.from_user.id)
    payment = yookassa.Payment.find_one(callback_data.pay_id)
    name = f'{callback.from_user.first_name} @{callback.from_user.username if callback.from_user.username else None}'
    if payment.status == 'succeeded':
        if user:
            await db_manager.update_user(user_id=callback.from_user.id, user_data={'subscription_status': True,
                                                                                  'subscription_start_date': start_date,
                                                                                  'subscription_end_date': end_date})
        else:
            await db_manager.add_user(user_data={'user_id': callback.from_user.id,
                                                 'telegram_id': callback.from_user.id,
                                                 'username': name,
                                                 'subscription_status': True,
                                                 'subscription_start_date': start_date,
                                                 'subscription_end_date': end_date})
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=get_photo(),
            caption=lexicon['buy'].format(start_date=start_date.strftime('%d-%m-%y'),
                                                        end_date=end_date.strftime('%d-%m-%y'))
        ),
        reply_markup=None
    )
    await bot.send_message(chat_id=int(admin_id()),
                           text=lexicon['new_user'].format(user_full_name=name))