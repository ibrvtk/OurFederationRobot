from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.data import report_data



kb_start_menu = ReplyKeyboardMarkup(keyboard=[
    # Клавиатура для handlers.py: cmd_start() . Навигатор, который всегда видно в ЛС.
    [KeyboardButton(text="👤 Профиль")],
    [KeyboardButton(text="🎩 Донат")]
],
resize_keyboard=True)


async def kb_profile_connect(user_id: int) -> InlineKeyboardBuilder:
    '''
    *Клавиатура для `handlers.py`: `cmd_profile()`.*
    Для человека, который ещё не привязал свой майнкрафт-никнейм к телеграм-аккаунту.
    '''
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.add(InlineKeyboardButton(
        text="🔗 Привязать майнкрафт-никнейм",
        callback_data=f"profile_connect_{user_id}"
    ))

    return inline_keyboard.adjust(1).as_markup()

async def kb_profile_connect_create_user(user_id: int) -> InlineKeyboardBuilder:
    '''
    *Клавиатура для `handlers.py`: `cmd_profile()`.*
    Вызывается тогда, когда никнейм уже был введён, и ожидается, что игрок совершил подтверждение в игре.
    '''
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.add(InlineKeyboardButton(
        text="✅ Я привязал",
        callback_data=f"profile_connect_create_{user_id}"
    ))

    return inline_keyboard.adjust(1).as_markup()

async def kb_profile_reputation(user_id: int, reputation_id: int) -> InlineKeyboardBuilder:
    '''
    *Клавиатура для `handlers.py`: `cmd_profile()`.*
    Клавиатура для других людей, с помощью которой можно повышать или понижать репутацию того, с кем она связана.
    '''
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.add(InlineKeyboardButton(
        text="➕",
        callback_data=f"profile_plusrep_{user_id}_{reputation_id}"
    ))
    inline_keyboard.add(InlineKeyboardButton(
        text="✨",
        callback_data=f"profile_rep"
    ))
    inline_keyboard.add(InlineKeyboardButton(
        text="➖",
        callback_data=f"profile_minusrep_{user_id}_{reputation_id}"
    ))

    return inline_keyboard.adjust(3).as_markup()


async def kb_report_maingroup(report_id: int) -> InlineKeyboardBuilder:
    '''
    *Клавиатура для `handlers.py`: `cmd_report()`. Устанавливается в публичном чате.*  
    '''
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.add(InlineKeyboardButton(
        text="🔴 Бан",
        callback_data=f"report_ban_{report_id}"
    ))
    inline_keyboard.add(InlineKeyboardButton(
        text="🔇 Мут",
        callback_data=f"report_mute_{report_id}"
    ))
    inline_keyboard.add(InlineKeyboardButton(
        text="➖ Сообщение",
        callback_data=f"report_delete_{report_id}"
    ))

    inline_keyboard.add(InlineKeyboardButton(
        text="🗓 Отметить проверенным",
        callback_data=f"report_check_{report_id}"
    ))

    return inline_keyboard.adjust(3).as_markup()

async def kb_report_admingroup(report_id: int) -> InlineKeyboardBuilder:
    '''
    *Клавиатура для `handlers.py`: `cmd_report()`. Устанавливается в админском чате.*  
    '''
    inline_keyboard = InlineKeyboardBuilder()

    chat_id = report_data[report_id].chat_id
    is_from_group = report_data[report_id].is_from_group
    user_message_id = report_data[report_id].user_message_id
    chat_id = str(chat_id).replace("-100", "") if is_from_group else None
    inline_keyboard.add(InlineKeyboardButton(
        text="Перейти к сообщению",
        url=f"https://t.me/c/{chat_id}/{user_message_id}"
    ))

    inline_keyboard.add(InlineKeyboardButton(
        text="🗓 Отметить проверенным",
        callback_data=f"report_check_{report_id}"
    ))

    return inline_keyboard.adjust(1).as_markup()