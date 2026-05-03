from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔞 ПОЛУЧИТЬ ДОСТУП", callback_data="buy")
    builder.button(text="📋 ОТЗЫВЫ", callback_data="reviews")
    builder.button(text="📱 WEB-ПРИЛОЖЕНИЕ", callback_data="webapp")
    builder.adjust(1)
    return builder.as_markup()

def reviews_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔞 ПОЛУЧИТЬ ДОСТУП", callback_data="buy")
    builder.button(text="◀️ НАЗАД", callback_data="start")
    builder.adjust(1)
    return builder.as_markup()

def payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Я ОПЛАТИЛ", callback_data="paid")
    builder.button(text="◀️ НАЗАД", callback_data="start")
    builder.adjust(1)
    return builder.as_markup()

def admin_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="💰 ПЛАТЕЖИ", callback_data="admin_payments")
    builder.button(text="👥 ПОЛЬЗОВАТЕЛИ", callback_data="admin_users")
    builder.button(text="📢 РАССЫЛКА", callback_data="admin_broadcast")
    builder.button(text="🚫 БАН", callback_data="admin_ban")
    builder.adjust(2, 2)
    return builder.as_markup()

def admin_payments_keyboard(payments):
    builder = InlineKeyboardBuilder()
    for p in payments[:10]:
        builder.button(text=f"✅ #{p['id']} — {p['amount']}₽", callback_data=f"confirm_{p['id']}")
    builder.button(text="◀️ НАЗАД", callback_data="admin")
    builder.adjust(1)
    return builder.as_markup()