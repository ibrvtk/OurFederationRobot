from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

from config import (
    BOT, FCMD_PREFIX,
    SUPERADMINS_ID,
    MAINGROUP_ID, MAINGROUP_USERNAME
)

from functions import (
    print_error, print_other,
    get_user_user
)

from databases.profiles import create_user
from databases.profiles.nicknames import read_by_user_id, read_by_user_username

from datetime import datetime


rt = Router()



@rt.message(F.from_user.id.in_(SUPERADMINS_ID), Command("daiop"))
async def cmd_daiop(message: Message): # Временная команда. Добавляет человека в БД. Только для админов.
    await create_user(message.from_user.id, "test", int(datetime.now().timestamp()))
    await print_other("(i) ")


@rt.message(F.text.lower() == "бот")
async def fcmd_check(message: Message):
    '''Проверка работоспособности бота и связи с телеграмом.'''
    try:
        await message.reply("✅ На месте")
    except Exception as e:
        await print_error(f"app/handlers.py: fcmd_check(): {e}.")


@rt.message(F.chat.type == "private", Command("start"))
async def cmdStart(message: Message):
    '''Карта команд.'''
    await message.reply(
        f"<b><code>{FCMD_PREFIX}профиль</code></b> — Привязанный аккаунт, статистика, РП-информация <i>(статус в законе, партия и так далее)</i>.\n\n"
        f"<b><code>{FCMD_PREFIX}донат</code> или /donate</b> — Управление балансом, донат-меню.\n\n"
        f"<b><code>{FCMD_PREFIX}жалоба</code> или /report</b> — Пожаловаться на игрока."
    )


@rt.message(F.text.lower().startswith(f"{FCMD_PREFIX}профиль"))
async def fcmd_profile(message: Message):
    '''Привязанный аккаунт, статистика, РП-информация *(статус в законе, партия и так далее)*.'''
    text = ""
    user_user = ""
    args = message.text.split(" ")

    if message.reply_to_message and len(args) == 1:
        # Если ответ на сообщение другого человека.
        user_data = await read_by_user_id(message.reply_to_message.from_user.id)
        user_user = await get_user_user(message.reply_to_message.from_user.id)

    elif len(args) == 1:
        # Свой профиль.
        user_data = await read_by_user_id(message.from_user.id)
        user_user = await get_user_user(message.from_user.id)

    elif len(args) == 2:
        # Если указан @юзернейм или TG-ID.
        if args[1].startswith("@"):
            user_username = args[1].replace("@", "")
            user_data = await read_by_user_username(user_username)
            user_user = await get_user_user(int(user_data[0]))
        else:
            try:
                user_data = await read_by_user_id(int(args[1]))
                user_user = await get_user_user(int(args[1]))
            except ValueError:
                await message.reply("❌ <b>Ошибка.</b> Неккоректный TG-ID.")
                return

    else:
        # Ниодин из вариантов.
        await message.reply("❌ <b>Ошибка.</b> Неверный ввод команды.")
        return

    if not user_data:
        await message.reply(f"👻 <b>{user_user} не игрок.</b>")
        return
    
    registration_date = datetime.fromtimestamp(user_data[3]).strftime("%d.%m.%Y %H:%M")
    text = (
        f"ℹ <b>Инфа {user_user}</b>\n\n"
        f"🔖 <b>Майнкрафт-никнейм:</b> {user_data[2]}\n"
        f"🗓️ <b>Дата регистрации на сервере:</b> {registration_date}"
    )

    await message.reply(text)