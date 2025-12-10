from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from config import BOT
from functions import (
    print_error,
    get_user_user,
    get_reputation_as_list,
    get_full_data
)

from app.dicts import reputation_data, report_data
from app.keyboards import kb_profile_reputation

from databases.players.nicknames import read_by_user_id as players_nicknames_read_by_user_id
from databases.players.roleplays import update_reputation as players_roleplays_update_reputation

from datetime import datetime



rt = Router()



@rt.callback_query(F.data.startswith("profile_plusrep_"))
async def cb_profile_plusrep(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[2])
    reputation_id = int(callback.data.split("_")[3])

    if reputation_id != reputation_data[user_id].reputation_id:
        await callback.answer("❌ Это старое сообщение. Вызовите новое")
        return

    from_user_id = callback.from_user.id

    if user_id == from_user_id:
        await callback.answer("❌ Ты нарцисс")
        return

    nicknames_from_user_data = await players_nicknames_read_by_user_id(from_user_id)
    if not nicknames_from_user_data:
        await callback.answer("❌ Ты не игрок")
        return

    chat_id = reputation_data[user_id].chat_id
    profile_message_id = reputation_data[user_id].profile_message_id
    text = reputation_data[user_id].profile_message_text

    reputation_list = await get_reputation_as_list(user_id)

    if from_user_id in reputation_list:
        await callback.answer("❌ Вы уже дали репутацию этому человеку")
        return

    reputation_str = await get_reputation_as_list(user_id=user_id, return_str=True)
    if reputation_str == "None":
        await callback.answer("✨ Вы первый!")

    new_reputation = await get_reputation_as_list(
        user_id=user_id,
        return_str=True,
        return_with_user_id=from_user_id
        )
    await players_roleplays_update_reputation(user_id, new_reputation)

    # Вывод.
    user_data = await get_full_data(user_id, True)
    from_user_user = await get_user_user(from_user_id)
    reputation_int = await get_reputation_as_list(user_id=user_id, return_int=True)

    text = (
        f"👤 <b>Профиль {user_data['user_user']}</b> ⦁ {reputation_int}✨\n\n"
        f"🔖 <b>Майнкрафт-никнейм:</b> {user_data['nicknames']['minecraft_nickname']}\n"
        f"🗓️ <b>Дата регистрации на сервере:</b> {user_data['nicknames']['registration_date']}\n\n"
        f"⛓ <b>Заключённый</b>: {user_data['roleplays']['is_prisoner']}\n"
        f"✊ <b>Восставший</b>: {user_data['roleplays']['is_rebel']}\n"
        f"🪖 <b>Военный</b>: {user_data['roleplays']['is_military']}\n"
        f"🪪 <b>Членство в партии</b>: {user_data['roleplays']['party_membership']}\n"
    )

    await BOT.edit_message_text(
        chat_id=chat_id,
        message_id=profile_message_id,
        text=text,
        reply_markup=await kb_profile_reputation(user_id, reputation_id)
    )
    await BOT.send_message(
        chat_id=user_id,
        text=f"✨ {from_user_user} дал Вам репутацию :)"
    )
    await callback.answer("✨ Вы дали репутацию")

@rt.callback_query(F.data == "profile_rep")
async def cb_profile_rep(callback: CallbackQuery):
    await callback.answer(
        text=(
            "✨ Это репутация.\n"
            "Пока-что ни на что не влияет, но существует.\n"
            "Она не может уйти в минус.\n"
            "Человеку приходит уведомление, когда его репутацию меняют.\n"
            "Менять репутацию могут только игроки.\n:3"
        ),
        show_alert=True
    )

@rt.callback_query(F.data.startswith("profile_minusrep_"))
async def cb_profile_minusrep(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[2])
    reputation_id = int(callback.data.split("_")[3])

    if reputation_id != reputation_data[user_id].reputation_id:
        await callback.answer("❌ Это старое сообщение. Вызовите новое")
        return

    from_user_id = callback.from_user.id

    if user_id == from_user_id:
        await callback.answer("❌ Хватить ненавидеть себя")
        return

    nicknames_from_user_data = await players_nicknames_read_by_user_id(from_user_id)
    if not nicknames_from_user_data:
        await callback.answer("❌ Ты не игрок")
        return

    chat_id = reputation_data[user_id].chat_id
    profile_message_id = reputation_data[user_id].profile_message_id
    text = reputation_data[user_id].profile_message_text

    reputation_list = await get_reputation_as_list(user_id)

    if from_user_id not in reputation_list:
        await callback.answer("❌ Ты ничего не дал, чтобы забирать")
        return

    new_reputation = await get_reputation_as_list(
        user_id=user_id, 
        return_str=True, 
        return_without_user_id=from_user_id
    )
    
    # В случае, если после удаления список стал пустым.
    if not new_reputation:
        new_reputation = "None"
    
    await players_roleplays_update_reputation(user_id, new_reputation)

    # Вывод.
    user_data = await get_full_data(user_id, True)
    from_user_user = await get_user_user(from_user_id)
    reputation_int = await get_reputation_as_list(user_id=user_id, return_int=True)

    text = (
        f"👤 <b>Профиль {user_data['user_user']}</b> ⦁ {reputation_int}✨\n\n"
        f"🔖 <b>Майнкрафт-никнейм:</b> {user_data['nicknames']['minecraft_nickname']}\n"
        f"🗓️ <b>Дата регистрации на сервере:</b> {user_data['nicknames']['registration_date']}\n\n"
        f"⛓ <b>Заключённый</b>: {user_data['roleplays']['is_prisoner']}\n"
        f"✊ <b>Восставший</b>: {user_data['roleplays']['is_rebel']}\n"
        f"🪖 <b>Военный</b>: {user_data['roleplays']['is_military']}\n"
        f"🪪 <b>Членство в партии</b>: {user_data['roleplays']['party_membership']}\n"
    )

    await BOT.edit_message_text(
        chat_id=chat_id,
        message_id=profile_message_id,
        text=text,
        reply_markup=await kb_profile_reputation(user_id, reputation_id)
    )
    await BOT.send_message(
        chat_id=user_id,
        text=f"✨ {from_user_user} отнял репутацию :("
    )
    await callback.answer("✨ Вы забрали репутацию :(")


@rt.callback_query(F.data.startswith("report_check_"))
async def cb_report_check(callback: CallbackQuery):
    report_id = int(callback.data.split("_")[2])
    chat_id = report_data[report_id].chat_id
    reply_message_id = report_data[report_id].reply_message_id
    send_message_id = report_data[report_id].send_message_id
    target_id = report_data[report_id].target_id
    target_user = await get_user_user(target_id)
    user_id = report_data[report_id].user_id
    user_user = await get_user_user(user_id)
    admin_user = await get_user_user(callback.from_user.id)
    report_reason = report_data[report_id].report_reason

    send_message_text = (
        f"✅ Жалоба на {target_user} проверена.\n"
        f"🆔 <code>{target_id}</code>\n"
        f"Отправил: {user_user}\n"
        f"Проверил: {admin_user}"
    )
    if report_reason is not None:
        send_message_text = f"{send_message_text}\n💬 {report_reason}"

    try:
        await BOT.edit_message_text(
            chat_id=chat_id,
            message_id=reply_message_id,
            text="✅ Жалоба проверена",
            reply_markup=None
        )
        await BOT.edit_message_text(
            chat_id=chat_id,
            message_id=send_message_id,
            text=send_message_text,
            reply_markup=None
        )
    except TelegramBadRequest as e:
        error = str(e)
        if ["message can't be edited", "'NoneType' object has no attribute 'message_id'"] in error:
            pass
        else:
            await print_error(f"app/callbacks.py: cb_report_check(): {error}.")

    del report_data[report_id]


@rt.callback_query(F.data.startswith("report_delete_"))
async def cb_report_delete(callback: CallbackQuery):
    report_id = int(callback.data.split("_")[2])
    chat_id = report_data[report_id].chat_id
    target_message_id = report_data[report_id].target_message_id

    try:
        await BOT.delete_message(
            chat_id=chat_id,
            message_id=target_message_id
        )
    except TelegramBadRequest as e:
        error = str(e)
        if "message to delete not found" in error:
            pass
        else:
            await print_error(f"app/callbacks.py: cb_report_delete(): {error}.")