from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from data.texts import *
from data.keyboards import *
from database.models import get_user, create_user

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    user = get_user(message.from_user.id)
    if not user:
        create_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    await message.answer(START_TEXT.format(price=PRICE), reply_markup=start_keyboard())

@router.callback_query(F.data == "start")
async def back_start(call: CallbackQuery):
    await call.message.edit_text(START_TEXT.format(price=PRICE), reply_markup=start_keyboard())
    await call.answer()

@router.callback_query(F.data == "reviews")
async def reviews(call: CallbackQuery):
    await call.message.edit_text(REVIEWS_TEXT, reply_markup=reviews_keyboard())
    await call.answer()

@router.callback_query(F.data == "faq")
async def faq(call: CallbackQuery):
    await call.message.edit_text(FAQ_TEXT.format(price=PRICE), reply_markup=faq_keyboard())
    await call.answer()
