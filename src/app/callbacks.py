from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from config import BOT
from functions import (
    print_error,
    get_user_user
)

from app.dicts import report_data


rt = Router()



@rt.callback_query(F.data.startswith("report_check_"))
async def cb_report_check(callback: CallbackQuery):
    cb_data = callback.data.split("_")
    report_id = int(cb_data[2])
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

    del report_data[report_id]


@rt.callback_query(F.data.startswith("report_delete_"))
async def cb_report_check(callback: CallbackQuery):
    cb_data = callback.data.split("_")
    report_id = int(cb_data[2])
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
            await print_error(f"app/callbacks.py: cb_report_check(): {error}.")