from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder



async def keyboard_report_admingroup(message: Message, is_from_group: bool | None = True):
    '''
    *Клавиатура для `handlers.py`: `fcmd_report()`.*  
    `message_id` — TG-ID сообщения, на которое подаётся жалоба.
    '''
    message_id = message.message_id
    chat_id = str(message.chat.id).replace("-100", "")
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="Перейти к сообщению", url=f"https://t.me/c/{chat_id}/{message_id}")) if is_from_group else None
    keyboard.add(InlineKeyboardButton(text="🗓 Отметить проверенным", callback_data=f"report_check_{message_id}"))

    return keyboard.adjust(1).as_markup()

async def keyboard_report_maingroup(message: Message):
    '''
    *Клавиатура для `handlers.py`: `fcmd_report()`.*  
    `message_id` — TG-ID сообщения, на которое подаётся жалоба.
    '''
    message_id = message.message_id
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="🔴 Бан", callback_data=f"report_ban_{message_id}"))
    keyboard.add(InlineKeyboardButton(text="🔇 Мут", callback_data=f"report_mute_{message_id}"))
    keyboard.add(InlineKeyboardButton(text="➖ Сообщение", callback_data=f"report_delete_{message_id}"))
    keyboard.add(InlineKeyboardButton(text="🗓 Отметить проверенным", callback_data=f"report_check_{message_id}"))

    return keyboard.adjust(3).as_markup()