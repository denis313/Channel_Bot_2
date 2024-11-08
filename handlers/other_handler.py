# from aiogram import Router, F
# from aiogram.filters import CommandStart, StateFilter
# from aiogram.fsm.state import default_state
# from aiogram.types import Message
#
# from database.requests import DatabaseManager
# from keyboards import
# from lexicon import lexicon
# from config import db_config
#
# router = Router()
# router.message.filter(F.chat.type == 'private')
# dsn = db_config()
# db_manager = DatabaseManager(dsn=dsn)
#
#
# @router.message(CommandStart(), StateFilter(default_state))
# async def start_command(message: Message):
#     await db_manager.create_tables()
#     await message.answer(lexicon['start'], reply_markup=keyboard_buy)
