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

from datetime import datetime


rt = Router()



@rt.message(F.from_user.id.in_(SUPERADMINS_ID), Command("daiop"))
async def cmd_daiop(message: Message): # Временная команда. Добавляет человека в БД. Только для админов.
    await create_user(message.from_user.id, "test", int(datetime.now().timestamp()))


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
    from databases.profiles.nicknames import (
        read_by_user_id as nicknames_read_by_user_id,
        read_by_user_username as nicknames_read_by_user_username
    )
    from databases.profiles.roleplays import read_by_user_id as roleplays_read_by_user_id

    args = message.text.split(" ")

    if message.reply_to_message and len(args) == 1:
        # Если ответ на сообщение другого человека.
        nicknames_user_data = await nicknames_read_by_user_id(message.reply_to_message.from_user.id)
        roleplays_user_data = await roleplays_read_by_user_id(message.reply_to_message.from_user.id)
        user_user = await get_user_user(message.reply_to_message.from_user.id)

    elif len(args) == 1:
        # Свой профиль.
        nicknames_user_data = await nicknames_read_by_user_id(message.from_user.id)
        roleplays_user_data = await roleplays_read_by_user_id(message.from_user.id)
        user_user = await get_user_user(message.from_user.id)

    elif len(args) == 2:
        # Если указан @юзернейм или TG-ID.
        if args[1].startswith("@"):
            user_username = args[1].replace("@", "")
            nicknames_user_data = await nicknames_read_by_user_username(user_username)
            roleplays_user_data = await roleplays_read_by_user_id(int(nicknames_user_data[0]))
            user_user = await get_user_user(int(nicknames_user_data[0]))
        else:
            try:
                nicknames_user_data = await nicknames_read_by_user_id(int(args[1]))
                roleplays_user_data = await roleplays_read_by_user_id(int(args[1]))
                user_user = await get_user_user(int(args[1]))
            except ValueError:
                await message.reply("❌ <b>Ошибка.</b> Неккоректный TG-ID.")
                return

    else:
        # Ниодин из вариантов.
        await message.reply("❌ <b>Ошибка.</b> Неверный ввод команды.")
        return

    if not nicknames_user_data:
        await message.reply(f"👻 <b>{user_user} не игрок.</b>")
        return
    
    registration_date = datetime.fromtimestamp(nicknames_user_data[3]).strftime("%d.%m.%Y %H:%M")
    is_prisoner = "Нет" if roleplays_user_data[1] == 0 else "Да"
    is_rebel = "Нет" if roleplays_user_data[2] == 0 else "Да"
    is_military = "Нет" if roleplays_user_data[3] == 0 else "Да"
    party_membership = "Нигде не состоит" if roleplays_user_data[4] == "None" else f"{roleplays_user_data[4]}"

    text = (
        f"ℹ <b>Инфа {user_user}</b>\n\n"
        f"🔖 <b>Майнкрафт-никнейм:</b> {nicknames_user_data[2]}\n"
        f"🗓️ <b>Дата регистрации на сервере:</b> {registration_date}\n\n"
        f"⛓ <b>Заключённый</b>: {is_prisoner}\n"
        f"✊ <b>Восставший</b>: {is_rebel}\n"
        f"🪖 <b>Военный</b>: {is_military}\n"
        f"🪪 <b>Членство в партии</b>: {party_membership}\n"
    )

    await message.reply(text)