from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo


def start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔞 ПОЛУЧИТЬ ДОСТУП", callback_data="buy")
    builder.button(text="📋 ОТЗЫВЫ", callback_data="reviews")
    builder.button(text="❓ КАК ЭТО РАБОТАЕТ", callback_data="faq")
    builder.button(text="📱 WEB-ПРИЛОЖЕНИЕ", web_app=WebAppInfo(url="https://nikojkinov-blip.github.io/qwezo/"))
    builder.adjust(1)
    return builder.as_markup()


def reviews_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔞 ПОЛУЧИТЬ ДОСТУП", callback_data="buy")
    builder.button(text="◀️ НАЗАД", callback_data="start")
    builder.adjust(1)
    return builder.as_markup()


def faq_keyboard():
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


def after_payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="📞 ПОДДЕРЖКА", url="https://t.me/MultiAccessHelp")
    builder.button(text="◀️ НА ГЛАВНУЮ", callback_data="start")
    builder.adjust(1)
    return builder.as_markup()


def admin_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="📊 СТАТИСТИКА", callback_data="admin_stats")
    builder.button(text="💰 ПЛАТЕЖИ", callback_data="admin_payments")
    builder.button(text="👥 ПОЛЬЗОВАТЕЛИ", callback_data="admin_users")
    builder.button(text="📢 РАССЫЛКА", callback_data="admin_broadcast")
    builder.button(text="❌ ЗАКРЫТЬ", callback_data="close")
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def admin_payments_keyboard(payments):
    builder = InlineKeyboardBuilder()
    for p in payments[:10]:
        builder.button(
            text=f"✅ #{p['id']} — {p['amount']}₽",
            callback_data=f"confirm_{p['id']}"
        )
    builder.button(text="◀️ НАЗАД", callback_data="admin")
    builder.adjust(1)
    return builder.as_markup()


def admin_back_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="◀️ НАЗАД", callback_data="admin")
    return builder.as_markup()


def webapp_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="📱 ОТКРЫТЬ", web_app=WebAppInfo(url="https://nikojkinov-blip.github.io/qwezo/"))
    builder.button(text="◀️ НАЗАД", callback_data="start")
    builder.adjust(1)
    return builder.as_markup()
