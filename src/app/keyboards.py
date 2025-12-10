from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.dicts import report_data



kb_start_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="👤 Профиль")],
    [KeyboardButton(text="🎩 Донат")]
],
resize_keyboard=True)


async def kb_profile_reputation(user_id: int, reputation_id: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
        text="➕",
        callback_data=f"profile_plusrep_{user_id}_{reputation_id}"
    ))
    keyboard.add(InlineKeyboardButton(
        text="✨",
        callback_data=f"profile_rep"
    ))
    keyboard.add(InlineKeyboardButton(
        text="➖",
        callback_data=f"profile_minusrep_{user_id}_{reputation_id}"
    ))

    return keyboard.adjust(3).as_markup()


async def kb_report_maingroup(report_id: int):
    '''
    *Клавиатура для `handlers.py`: `fcmd_report()`. Для админского чата.*  
    '''
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
        text="🔴 Бан",
        callback_data=f"report_ban_{report_id}"
    ))
    keyboard.add(InlineKeyboardButton(
        text="🔇 Мут",
        callback_data=f"report_mute_{report_id}"
    ))
    keyboard.add(InlineKeyboardButton(
        text="➖ Сообщение",
        callback_data=f"report_delete_{report_id}"
    ))

    keyboard.add(InlineKeyboardButton(
        text="🗓 Отметить проверенным",
        callback_data=f"report_check_{report_id}"
    ))

    return keyboard.adjust(3).as_markup()

async def kb_report_admingroup(report_id: int):
    '''
    *Клавиатура для `handlers.py`: `fcmd_report()`. Для публичного чата.*  
    '''
    keyboard = InlineKeyboardBuilder()

    chat_id = report_data[report_id].chat_id
    is_from_group = report_data[report_id].is_from_group
    user_message_id = report_data[report_id].user_message_id
    chat_id = str(chat_id).replace("-100", "") if is_from_group else None
    keyboard.add(InlineKeyboardButton(
        text="Перейти к сообщению",
        url=f"https://t.me/c/{chat_id}/{user_message_id}"
    ))

    keyboard.add(InlineKeyboardButton(
        text="🗓 Отметить проверенным",
        callback_data=f"report_check_{report_id}"
    ))

    return keyboard.adjust(1).as_markup()