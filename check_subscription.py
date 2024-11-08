import logging
from datetime import date

from bot import bot
from config import db_config
from database.requests import DatabaseManager
from keyboards import keyboard_prepayment
from lexicon import lexicon
from service import get_photo, create_payment

logger = logging.getLogger(__name__)
dsn = db_config()
db_manager = DatabaseManager(dsn=dsn)


async def check_status():
    logging.debug(f'check_status')
    now = date.today()
    users = await db_manager.get_users()
    for user in users:
        url, id_payment = create_payment(amount=2000,
                                         description="Оплата закрытого телеграм канала",
                                         chat_id=user.user_id)
        kb = keyboard_prepayment(url=url, id_payment=id_payment)
        date_user = user.subscription_end_date
        days = date_user - now
        print(days)
        if abs(days.days) == 3:
            await db_manager.update_user(user_id=user.user_id, user_data={'subscription_status': False})
            await bot.send_photo(chat_id=user.user_id, photo=get_photo(), caption=lexicon['end_sub'], reply_markup=kb)
        elif abs(days.days) <= 0:
            await db_manager.delete_user(user_id=user.user_id)
            await bot.send_message(chat_id=user.user_id, text=lexicon['del_user'], reply_markup=kb)
            await bot.ban_chat_member(chat_id=-1002299872725, user_id=user.user_id)
            await bot.unban_chat_member(chat_id=-1002299872725, user_id=user.user_id)
            logging.debug(f'Kick user by id={user.user_id}')

