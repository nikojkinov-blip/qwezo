from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo


def start_keyboard():
    """Главное меню"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🔞 ПОЛУЧИТЬ ДОСТУП", callback_data="buy")
    builder.button(text="📋 ОТЗЫВЫ", callback_data="reviews")
    builder.button(text="📱 WEB-ПРИЛОЖЕНИЕ", web_app=WebAppInfo(url="https://nikojkinov-blip.github.io/qwezo/"))
    builder.button(text="❓ КАК ЭТО РАБОТАЕТ", callback_data="faq")
    builder.adjust(1)
    return builder.as_markup()


def reviews_keyboard():
    """Клавиатура после отзывов"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🔞 ПОЛУЧИТЬ ДОСТУП", callback_data="buy")
    builder.button(text="◀️ НАЗАД", callback_data="start")
    builder.adjust(1)
    return builder.as_markup()


def faq_keyboard():
    """Клавиатура после FAQ"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🔞 ПОЛУЧИТЬ ДОСТУП", callback_data="buy")
    builder.button(text="◀️ НАЗАД", callback_data="start")
    builder.adjust(1)
    return builder.as_markup()


def payment_keyboard():
    """Клавиатура оплаты"""
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Я ОПЛАТИЛ", callback_data="paid")
    builder.button(text="◀️ НАЗАД", callback_data="start")
    builder.adjust(1)
    return builder.as_markup()


def after_payment_keyboard():
    """Клавиатура после оплаты"""
    builder = InlineKeyboardBuilder()
    builder.button(text="📞 СВЯЗАТЬСЯ С ПОДДЕРЖКОЙ", url="https://t.me/MultiAccessHelp")
    builder.button(text="📋 МОИ ПОКУПКИ", callback_data="my_purchases")
    builder.button(text="◀️ НА ГЛАВНУЮ", callback_data="start")
    builder.adjust(1)
    return builder.as_markup()


def admin_keyboard():
    """Админ-панель"""
    builder = InlineKeyboardBuilder()
    builder.button(text="📊 СТАТИСТИКА", callback_data="admin_stats")
    builder.button(text="💰 ПЛАТЕЖИ", callback_data="admin_payments")
    builder.button(text="👥 ПОЛЬЗОВАТЕЛИ", callback_data="admin_users")
    builder.button(text="📢 РАССЫЛКА", callback_data="admin_broadcast")
    builder.button(text="🚫 БАН ПОЛЬЗОВАТЕЛЯ", callback_data="admin_ban")
    builder.button(text="✅ РАЗБАН", callback_data="admin_unban")
    builder.button(text="🔄 ОБНОВИТЬ", callback_data="admin")
    builder.button(text="❌ ЗАКРЫТЬ", callback_data="close")
    builder.adjust(2, 2, 2, 1, 1)
    return builder.as_markup()


def admin_payments_keyboard(payments: list):
    """Клавиатура с ожидающими платежами"""
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
    """Кнопка назад в админку"""
    builder = InlineKeyboardBuilder()
    builder.button(text="◀️ НАЗАД В АДМИНКУ", callback_data="admin")
    return builder.as_markup()


def users_keyboard(users: list):
    """Клавиатура с пользователями"""
    builder = InlineKeyboardBuilder()
    for u in users[:10]:
        status = "💎" if u.get('paid') else "⏳"
        ban = "🚫" if u.get('banned') else ""
        name = f"@{u.get('username', '?')}"
        builder.button(
            text=f"{status}{ban} {name}",
            callback_data=f"userinfo_{u['user_id']}"
        )
    builder.button(text="◀️ НАЗАД", callback_data="admin")
    builder.adjust(1)
    return builder.as_markup()


def user_actions_keyboard(user_id: int, is_banned: bool = False, is_paid: bool = False):
    """Действия с пользователем"""
    builder = InlineKeyboardBuilder()
    if not is_paid:
        builder.button(text="💎 ВЫДАТЬ ДОСТУП", callback_data=f"give_access_{user_id}")
    if is_banned:
        builder.button(text="✅ РАЗБАНИТЬ", callback_data=f"unban_{user_id}")
    else:
        builder.button(text="🚫 ЗАБАНИТЬ", callback_data=f"ban_{user_id}")
    builder.button(text="📩 НАПИСАТЬ", url=f"tg://user?id={user_id}")
    builder.button(text="◀️ НАЗАД", callback_data="admin_users")
    builder.adjust(1)
    return builder.as_markup()


def ban_keyboard():
    """Клавиатура для бана"""
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ ОТМЕНА", callback_data="admin")
    return builder.as_markup()


def broadcast_keyboard():
    """Клавиатура для рассылки"""
    builder = InlineKeyboardBuilder()
    builder.button(text="📢 ВСЕМ ПОЛЬЗОВАТЕЛЯМ", callback_data="bc_all")
    builder.button(text="💎 ТОЛЬКО ОПЛАТИВШИМ", callback_data="bc_paid")
    builder.button(text="⏳ НЕ ОПЛАТИВШИМ", callback_data="bc_unpaid")
    builder.button(text="◀️ ОТМЕНА", callback_data="admin")
    builder.adjust(2, 1, 1)
    return builder.as_markup()


def broadcast_confirm_keyboard():
    """Подтверждение рассылки"""
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ ОТПРАВИТЬ", callback_data="bc_send")
    builder.button(text="❌ ОТМЕНА", callback_data="admin")
    builder.adjust(1)
    return builder.as_markup()


def cancel_keyboard():
    """Отмена действия"""
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ ОТМЕНА", callback_data="start")
    return builder.as_markup()


def close_keyboard():
    """Закрыть сообщение"""
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ ЗАКРЫТЬ", callback_data="close")
    return builder.as_markup()


def webapp_keyboard():
    """Клавиатура с WebApp"""
    builder = InlineKeyboardBuilder()
    builder.button(text="📱 ОТКРЫТЬ ПРИЛОЖЕНИЕ", web_app=WebAppInfo(url="https://nikojkinov-blip.github.io/qwezo/"))
    builder.button(text="◀️ НАЗАД", callback_data="start")
    builder.adjust(1)
    return builder.as_markup()
