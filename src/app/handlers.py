from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

from config import (
    BOT, FCMD_PREFIX,
    ADMINGROUP_ID
)
from functions import (
    print_error,
    get_user_id, get_user_user, is_bot, get_full_data
)

from app.data import (
    reputation_data, ReputationDataclass,
    report_data, ReportDataclass
)
from app.keyboards import (
    kb_start_menu,
    kb_profile_connect, kb_profile_reputation,
    kb_report_admingroup, kb_report_maingroup
)

from datetime import datetime


rt = Router()



@rt.message(F.text.lower() == "бот")
async def fcmd_check(message: Message):
    '''Проверка работоспособности бота и связи с телеграмом.'''
    try:
        await message.reply("✅ На месте")
    except TelegramBadRequest as e:
        await print_error(f"app/handlers.py: fcmd_check(): {e}.")


@rt.message(F.chat.type == "private", F.text.lower().startswith("начать"))
@rt.message(F.chat.type == "private", F.text.lower().startswith(f"{FCMD_PREFIX}начать"))
@rt.message(F.chat.type == "private", Command("start"))
async def cmd_start(message: Message):
    '''Карта бота.'''
    text = (
        "🦅 <b><a href='https://t.me/OurFederationRobot'>Робот Федерации</a> приветствует Вас!</b>\n"
        "Я могу предложить следующие темы:\n\n"
        "⦁ <code>профиль</code> — Привязанный аккаунт, РП-информация, статистика;\n"
        "⦁ <code>настройки</code> — Настройка бота и некоторых плагинов сервераж\n"
        "⦁ <code>жалоба</code> — Пожаловаться на игрока или сообщение в чате;\n"
        "⦁ <code>донат</code> — Донат-меню, управление балансом. <i>В разработке</i>\n\n"
        "💬 Официальный <a href='https://t.me/OurFederationMC'>чат сервера</a>.\n"
        "🗺 Для вызова карты <i>(полезных быстрых)</i> команд, введите <code>помощь</code>."
    )
    await message.reply(
        text=text,
        reply_markup=kb_start_menu,
        disable_web_page_preview=True
    )

@rt.message(F.text.lower().startswith("помощь"))
@rt.message(F.text.lower().startswith(f"{FCMD_PREFIX}помощь"))
async def fcmd_help(message: Message):
    '''Карта команд.'''
    if message.chat.type == "private":
        await cmd_start(message)
        return

    bot_user = await BOT.get_me()
    text = (
        f"📖 <b>Помощь по функционалу бота<a href='https://t.me/OurFederationRobot'>{bot_user.full_name}</a></b>\n\n"
         "👤 <code>профиль</code> — Привязанный аккаунт, РП-информация, статистика;\n"
         "❗️ <code>жалоба</code> — Пожаловаться на игрока или сообщение в чате;\n"
         "🎩 <code>донат</code> — Донат-меню, управление балансом."
    )
    await message.reply(
        text=text,
        disable_web_page_preview=True
    )


@rt.message(F.text.lower().startswith("профиль"))
@rt.message(F.text.lower().startswith(f"{FCMD_PREFIX}профиль"))
@rt.message(F.chat.type == "private", F.text == "👤 Профиль")
@rt.message(Command('profile'))
async def cmd_profile(message: Message):
    '''
    Привязанный аккаунт, статистика, РП-информация *(статус в законе, партия и так далее)*.
    '''
    args = message.text.split(" ")
    user_id = message.from_user.id
    target_id = None

    if len(args) == 1:
        if message.reply_to_message:
            # Посмотреть профиль другого человека, путём ответа на его сообщение командой.
            target_id = message.reply_to_message.from_user.id

            if await is_bot(target_id):
                # Проверка: Если команда введена на бота.
                await message.delete()
                return

    if len(args) == 2 and not "👤 Профиль":
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
        await message.delete()
        return

    if user_id == target_id:
        # Проверка: Если команда введена на самого себя.
        await message.delete()
        return

    if target_id is not None:
        user_id = target_id

    user_data = await get_full_data(user_id, True)

    if not user_data:
        user_user = await get_user_user(user_id)
        await message.reply(
            text=f"👻 <b>{user_user} не игрок.</b>",
            reply_markup=await kb_profile_connect(user_id) if message.chat.type == "private" else None
            )
        return

    # Вывод.
    text = (
        f"👤 <b>Профиль {user_data['user_user']}</b> ⦁ {user_data['roleplays']['reputation']}✨\n\n"
        f"🔖 <b>Майнкрафт-никнейм:</b> {user_data['nicknames']['minecraft_nickname']}\n"
        f"🗓️ <b>Дата регистрации на сервере:</b> {user_data['nicknames']['registration_date']}\n\n"
        f"⛓ <b>Заключённый</b>: {user_data['roleplays']['is_prisoner']}\n"
        f"✊ <b>Восставший</b>: {user_data['roleplays']['is_rebel']}\n"
        f"🪖 <b>Военный</b>: {user_data['roleplays']['is_military']}\n"
        f"🪪 <b>Членство в партии</b>: {user_data['roleplays']['party_membership']}\n"
    )

    profile_message_obj = await message.reply(text)

    if message.chat.type == "private":
        return

    reputation_id = int(datetime.now().timestamp())
    chat_id = message.chat.id
    profile_message_id = profile_message_obj.message_id
    reputation_data[user_id] = ReputationDataclass(
        user_id,
        reputation_id,
        chat_id,
        profile_message_id,
        text
    )

    await BOT.edit_message_text(
        chat_id=chat_id,
        message_id=profile_message_id,
        text=text,
        reply_markup=await kb_profile_reputation(user_id, reputation_id)
    )


@rt.message(F.text.lower().startswith("жалоба"))
@rt.message(F.text.lower().startswith(f"{FCMD_PREFIX}жалоба"))
@rt.message(Command('report'))
async def cmd_report(message: Message):
    '''Пожаловаться на игрока.'''
    paragraphs = message.text.split("\n")
    args = []
    for i in paragraphs:
        words = i.split(" ")
        args.append(words)
    user_id = message.from_user.id
    target_id = None
    target_message_id = None
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

        target_message_id = message.reply_to_message.reply_to_message

        if len(paragraphs) == 2:
            report_reason = paragraphs[1]

    elif message.chat.type == "private":
        # Жалоба на игрока (только в личке).
        if len(args) < 2 or len(paragraphs) < 2:
            # Проверка: Недостаточно аргументов.
            await message.reply(
                "❌ <b>Неверный ввод команды.</b> Правильно:\n"
                "<blockquote><code>жалоба </code>[@юзернейм/TG-ID/майнкрафт-никнейм]\nОпишите причину</blockquote>"
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
    report_data[report_id] = ReportDataclass(
        report_id,
        user_id,
        target_id,
        user_message_id,
        target_message_id,
        reply_message_id,
        send_message_id,
        report_reason,
        is_from_group,
        chat_id
    )

    await BOT.edit_message_text(
        chat_id=chat_id,
        message_id=reply_message_id,
        text=reply_text,
        reply_markup=await kb_report_maingroup(report_id)
    )
    await BOT.edit_message_text(
        chat_id=chat_id,
        message_id=send_message_id,
        text=send_message_text,
        reply_markup=await kb_report_admingroup(report_id)
    )


# @rt.message(F.text.lower().startswith("донат"))
# @rt.message(F.text.lower().startswith(f"{FCMD_PREFIX}донат"))
# @rt.message(F.chat.type == "private", F.text == "🎩 Донат")
# @rt.message(Command('donate'))
# async def cmd_donate(message: Message):
#     '''Донат-меню, управление балансом.'''