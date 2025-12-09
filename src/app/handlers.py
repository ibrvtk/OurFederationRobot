from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

from config import (
    BOT, FCMD_PREFIX,
    SUPERADMINS_ID,
    ADMINGROUP_ID
)
from functions import (
    print_error,
    get_user_id, get_user_user, is_bot
)

from app.dicts import (
    report_data, report_dataclass
)
from app.keyboards import (
    keyboard_report_admingroup as report_admingroup,
    keyboard_report_maingroup as report_maingroup
)

from databases.profiles.nicknames import read_by_user_id as profiles_nicknames_read_by_user_id
from databases.profiles.roleplays import read_by_user_id as profiles_roleplays_read_by_user_id

from datetime import datetime


rt = Router()



@rt.message(F.from_user.id.in_(SUPERADMINS_ID), Command("daiop"))
async def cmd_daiop(message: Message): # Временная команда. Добавляет человека в БД. Только для админов.
    from databases.profiles import create_user as profiles_create_user
    await profiles_create_user(message.from_user.id, "test", int(datetime.now().timestamp()))


@rt.message(F.text.lower() == "бот")
async def fcmd_check(message: Message):
    '''Проверка работоспособности бота и связи с телеграмом.'''
    try:
        await message.reply("✅ На месте")
    except TelegramBadRequest as e:
        await print_error(f"app/handlers.py: fcmd_check(): {e}.")


@rt.message(F.chat.type == "private", Command("start"))
async def cmd_start(message: Message):
    '''Карта команд.'''
    await message.reply(
        f"<b><code>{FCMD_PREFIX}профиль</code></b> — Привязанный аккаунт, статистика, РП-информация <i>(статус в законе, партия и так далее)</i>.\n\n"
        f"<b><code>{FCMD_PREFIX}донат</code> или /donate</b> — Управление балансом, донат-меню.\n\n"
        f"<b><code>{FCMD_PREFIX}жалоба</code> или /report</b> — Пожаловаться на игрока."
    )


@rt.message(F.text.lower().startswith(f"{FCMD_PREFIX}профиль"))
async def fcmd_profile(message: Message):
    '''
    Привязанный аккаунт, статистика, РП-информация *(статус в законе, партия и так далее)*.
    '''
    args = message.text.split(" ")
    user_id = message.from_user.id
    target_id = None
    nicknames_data = None
    roleplays_data = None

    if len(args) == 1:
        if message.reply_to_message:
            # Посмотреть профиль другого человека, путём ответа на его сообщение командой.
            target_id = message.reply_to_message.from_user.id

            if await is_bot(target_id):
                # Проверка: Если команда введена на бота.
                await message.delete()
                return

    if len(args) == 2:
        # Посмотреть профиль другого человека, путём ввода его @юзернейма/TG-ID/майнкрафт-никнейма после команды.
        identifier = args[1]
        if identifier.isdigit():
            # TG-ID.
            target_id = int(identifier)
        else:
            # @юзернейм либо майнкрафт-никнейм.
            target_id = await get_user_id(identifier)
            if target_id is None:
                # Проверка: Удалось ли найти человека через БД (через функцию `get_user_id()`).
                await message.reply(
                    "❌ <b>Человек не найден.</b> Ни по @юзернейму, ни по майнкрафт-никнейму. "
                    "Проверьте правильность введённых данных."
                )
                return

    elif len(args) > 2:
        # Ни один из вариантов.
        await message.delete()
        return

    if user_id == target_id:
        # Проверка: Если команда введена на самого себя.
        await message.delete()
        return

    if target_id != 0:
        user_id = target_id

    nicknames_data = await profiles_nicknames_read_by_user_id(user_id)
    roleplays_data = await profiles_roleplays_read_by_user_id(user_id)
    user_user = await get_user_user(user_id)

    if not nicknames_data:
        await message.reply(f"👻 <b>{user_user} не игрок.</b>")
        return

    # Вывод.
    minecraft_nickname = nicknames_data[2]
    registration_date = datetime.fromtimestamp(nicknames_data[3]).strftime("%d.%m.%Y %H:%M")
    is_prisoner = "Нет" if roleplays_data[1] == 0 else "Да"
    is_rebel = "Нет" if roleplays_data[2] == 0 else "Да"
    is_military = "Нет" if roleplays_data[3] == 0 else "Да"
    party_membership = "Нигде не состоит" if roleplays_data[4] == "None" else f"{roleplays_data[4]}"

    await message.reply(
        f"ℹ <b>Инфа {user_user}</b>\n\n"
        f"🔖 <b>Майнкрафт-никнейм:</b> {minecraft_nickname}\n"
        f"🗓️ <b>Дата регистрации на сервере:</b> {registration_date}\n\n"
        f"⛓ <b>Заключённый</b>: {is_prisoner}\n"
        f"✊ <b>Восставший</b>: {is_rebel}\n"
        f"🪖 <b>Военный</b>: {is_military}\n"
        f"🪪 <b>Членство в партии</b>: {party_membership}\n"
    )


@rt.message(F.text.lower().startswith(f"{FCMD_PREFIX}жалоба"))
async def fcmd_report(message: Message):
    '''Пожаловаться на игрока.'''
    paragraphs = message.text.split("\n")
    args = []
    for i in paragraphs:
        words = i.split(" ")
        args.append(words)
    user_id = message.from_user.id
    target_id = None
    report_reason = None
    is_from_group = True

    if len(paragraphs) > 2:
        # Проверка: Если человек пишет лишние абзацы.
        await message.delete()
        return

    if message.chat.type in ["group", "supergroup"]:
        # Жалоба на сообщение (в группе).
        if not message.reply_to_message:
            # Проверка: Если человек просто написал команду, без цели.
            await message.delete()
            return

        target_id = message.reply_to_message.from_user.id

        if await is_bot(target_id):
            # Проверка: Если команда введена на бота.
            await message.delete()
            return

        if len(paragraphs) == 2:
            report_reason = paragraphs[1]

    elif message.chat.type == "private":
        # Жалоба на игрока (только в личке).
        if len(args) < 2 or len(paragraphs) < 2:
            # Проверка: Недостаточно аргументов.
            await message.reply(
                "❌ <b>Неверный ввод команды.</b> Правильно:\n"
                "<blockquote><code>!жалоба </code>[@юзернейм/TG-ID/майнкрафт-никнейм]\nОпишите причину</blockquote>"
            )
            return
        
        identifier = args[0][1]
        if identifier.isdigit():
            # TG-ID.
            target_id = int(identifier)
        else:
            # @юзернейм либо майнкрафт-никнейм.
            target_id = await get_user_id(identifier)
            if target_id is None:
                # Проверка: Удалось ли найти человека через БД (через функцию `get_user_id()`).
                await message.reply(
                    "❌ <b>Человек не найден.</b> Ни по @юзернейму, ни по майнкрафт-никнейму. "
                    "Проверьте правильность введённых данных."
                )
                return
        
        report_reason = paragraphs[1]
        is_from_group = False

    else:
        # Ни один из вариантов.
        await message.delete()
        return

    if user_id == target_id:
        # Проверка: Если команда введена на самого себя.
        await message.delete()
        return

    # Вывод.
    user_user = await get_user_user(user_id)
    target_user = await get_user_user(target_id)

    reply_text = (
        f"❗️ Жалоба на {target_user} отправлена\n"
        f"🆔 <code>{target_id}</code>\n"
        f"🗣 Отправил: {user_user}"
    )
    send_message_text = (
        f"❗️ <b>Жалоба на {target_user}</b>\n"
        f"🆔 <code>{target_id}</code>\n"
        f"🗣 Отправил: {user_user}"
    )

    if message.chat.type in ["group", "supergroup"]:
        if report_reason is not None:
            send_message_text = f"{send_message_text}\n💬 {report_reason}"

    elif message.chat.type == "private":
        reply_text = f"❗️ Жалоба на {target_user} отправлена"
        send_message_text = f"{send_message_text}\n💬 {report_reason}"

    reply_message_obj = await message.reply(reply_text)
    send_message_obj = await BOT.send_message(
        chat_id=ADMINGROUP_ID,
        text=send_message_text
        )

    report_id = int(datetime.now().timestamp())
    user_message_id = message.message_id
    reply_message_id = reply_message_obj.message_id
    send_message_id = send_message_obj.message_id
    chat_id = message.chat.id
    report_data[report_id] = report_dataclass(
        report_id=report_id,
        user_id=user_id,
        target_id=target_id,
        user_message_id=user_message_id,
        target_message_id=message.reply_to_message.message_id,
        reply_message_id=reply_message_id,
        send_message_id=send_message_id,
        report_reason=report_reason,
        is_from_group=is_from_group,
        chat_id=chat_id
    )

    await BOT.edit_message_text(
        chat_id=chat_id,
        message_id=reply_message_id,
        text=reply_text,
        reply_markup=await report_maingroup(report_id)
    )
    await BOT.edit_message_text(
        chat_id=chat_id,
        message_id=send_message_id,
        text=send_message_text,
        reply_markup=await report_admingroup(report_id)
    )

@rt.message(Command('report'))
async def cmd_report(message: Message):
    await fcmd_report(message)