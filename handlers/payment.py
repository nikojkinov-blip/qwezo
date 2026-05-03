from aiogram import Router, F
from aiogram.types import CallbackQuery
from datetime import datetime
from data.texts import *
from data.keyboards import *
from database.models import db, get_user
import os

router = Router()
ADMIN = int(os.getenv("ADMIN_ID", "0"))

@router.callback_query(F.data == "buy")
async def buy(call: CallbackQuery):
    user = get_user(call.from_user.id)
    if user and user.get('paid'):
        await call.answer("✅ У вас уже есть доступ!", show_alert=True)
        return
    
    await call.message.edit_text(
        PAYMENT_TEXT.format(price=PRICE, card=CARD, bank=BANK),
        reply_markup=payment_keyboard()
    )
    await call.answer()

@router.callback_query(F.data == "paid")
async def paid(call: CallbackQuery):
    db.insert('payments', {
        'user_id': call.from_user.id,
        'amount': PRICE,
        'status': 'pending',
        'created_at': datetime.now().isoformat()
    })
    
    if ADMIN:
        try:
            await call.bot.send_message(ADMIN, f"🔔 Новая оплата!\n👤 {call.from_user.id}\n💰 {PRICE}₽")
        except:
            pass
    
    await call.message.edit_text(AFTER_PAY_PENDING, reply_markup=after_payment_keyboard())
    await call.answer("✅ Заявка отправлена!", show_alert=True)
