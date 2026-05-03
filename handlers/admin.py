from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from data.texts import *
from data.keyboards import *
from database.models import get_pending_payments, confirm_payment, get_total_stats, get_user, db, create_user

router = Router()

def is_admin(user_id): return user_id == ADMIN_ID

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id): return
    stats = get_total_stats()
    pending = len(get_pending_payments())
    await message.answer(
        ADMIN_PANEL.format(users=stats['users'], paid=stats['paid'], pays=stats['pays'], revenue=stats['revenue'], pending=pending),
        reply_markup=admin_keyboard()
    )

@router.callback_query(F.data == "admin")
async def admin_back(call: CallbackQuery):
    if not is_admin(call.from_user.id): return
    stats = get_total_stats()
    pending = len(get_pending_payments())
    await call.message.edit_text(
        ADMIN_PANEL.format(users=stats['users'], paid=stats['paid'], pays=stats['pays'], revenue=stats['revenue'], pending=pending),
        reply_markup=admin_keyboard()
    )
    await call.answer()

@router.callback_query(F.data == "admin_payments")
async def admin_payments(call: CallbackQuery):
    if not is_admin(call.from_user.id): return
    payments = get_pending_payments()
    if not payments:
        await call.answer("Нет ожидающих платежей", show_alert=True)
        return
    text = "💰 <b>Ожидающие платежи:</b>\n\n"
    for p in payments[:10]:
        text += f"#{p['id']} | User: <code>{p['user_id']}</code> | {p['amount']}₽\n"
    await call.message.edit_text(text, reply_markup=admin_payments_keyboard(payments))
    await call.answer()

@router.callback_query(F.data.startswith("confirm_"))
async def confirm(call: CallbackQuery):
    if not is_admin(call.from_user.id): return
    payment_id = int(call.data.split("_")[1])
    confirm_payment(payment_id)
    
    pay = db.fetchone("SELECT * FROM payments WHERE id=?", (payment_id,))
    if pay:
        try:
            await call.bot.send_message(pay['user_id'], AFTER_PAY_SUCCESS)
        except: pass
    
    await call.message.edit_text(call.message.text + f"\n\n✅ #{payment_id} ПОДТВЕРЖДЁН!")
    await call.answer("✅ Подтверждён!")

@router.callback_query(F.data == "admin_users")
async def admin_users(call: CallbackQuery):
    if not is_admin(call.from_user.id): return
    users = db.fetchall("SELECT * FROM users ORDER BY joined_date DESC LIMIT 30")
    text = "👥 <b>Последние 30 пользователей:</b>\n\n"
    for u in users:
        status = "💎" if u.get('paid') else "⏳"
        text += f"{status} <code>{u['user_id']}</code> @{u.get('username','?')}\n"
    await call.message.edit_text(text, reply_markup=InlineKeyboardBuilder().button(text="◀️ НАЗАД", callback_data="admin").as_markup())
    await call.answer()

@router.callback_query(F.data == "admin_ban")
async def admin_ban(call: CallbackQuery):
    if not is_admin(call.from_user.id): return
    await call.message.edit_text("🚫 <b>БАН ПОЛЬЗОВАТЕЛЯ</b>\n\nВведите /ban ID", reply_markup=InlineKeyboardBuilder().button(text="◀️ НАЗАД", callback_data="admin").as_markup())
    await call.answer()

@router.message(Command("ban"))
async def ban_user(message: Message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()
    if len(args) < 2: await message.answer("/ban ID"); return
    user_id = int(args[1])
    db.update('users', {'banned': 1}, 'user_id=?', (user_id,))
    try: await message.bot.send_message(user_id, BAN_TEXT)
    except: pass
    await message.answer(f"🚫 {user_id} забанен!")

@router.message(Command("unban"))
async def unban_user(message: Message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()
    if len(args) < 2: return
    user_id = int(args[1])
    db.update('users', {'banned': 0}, 'user_id=?', (user_id,))
    await message.answer(f"✅ {user_id} разбанен!")

@router.message(Command("broadcast"))
async def broadcast(message: Message):
    if not is_admin(message.from_user.id): return
    text = message.text.replace("/broadcast ", "", 1)
    if text == "/broadcast": await message.answer("/broadcast ТЕКСТ"); return
    users = db.fetchall("SELECT user_id FROM users WHERE banned=0")
    sent = 0
    for u in users:
        try: await message.bot.send_message(u['user_id'], f"📢 {text}"); sent += 1
        except: pass
    await message.answer(f"✅ Отправлено: {sent}/{len(users)}")

from aiogram.utils.keyboard import InlineKeyboardBuilder