from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, InputMediaPhoto
from bot import bot
from database.requests import DatabaseManager
from keyboards import keyboard_prepayment
from lexicon import lexicon
from config import db_config
from service import create_payment, get_photo

router = Router()
router.message.filter(F.chat.type == 'private')
dsn = db_config()
db_manager = DatabaseManager(dsn=dsn)


@router.message(CommandStart(), StateFilter(default_state))
async def start_command(message: Message):
    await db_manager.create_tables()
    user = await db_manager.get_user(user_id=message.from_user.id)
    show_keyboard = True
    if not user:
        price = 4000
        text = lexicon['start']
    elif user.subscription_status is False:
        price = 1900
        text = lexicon['every_buy']
    else:
        price = 1900
        text = lexicon['already_buy']
        show_keyboard = False  # Не показываем клавиатуру, если подписка уже оформлена

    url, id_payment = create_payment(
        amount=price,
        description="Оплата закрытого телеграм канала",
        chat_id=message.from_user.id,
        name=message.from_user.first_name,
        phone=79785878778
    )

    # Создаём клавиатуру только при необходимости
    if show_keyboard:
        kb = keyboard_prepayment(url=url, id_payment=id_payment)
    else:
        kb = None  # Клавиатура не передаётся

    # Отправляем сообщение с или без клавиатуры в зависимости от условий
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=get_photo(),
        caption=text,
        reply_markup=kb
    )


