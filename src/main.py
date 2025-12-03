from aiogram import Dispatcher

from config import (
    BOT,
    ADMINGROUP_ID
)

from functions import print_error, print_other

from app.handlers import rt as handlers_rt

from databases.profiles import create_database

from asyncio import run#, create_task
from aiohttp import ClientSession


DP = Dispatcher()



async def main() -> None:
    '''Запуск бота.'''
    session = ClientSession()

    try:
        await print_other("(+) Запуск бота: Подключение к Телеграму...")
        # start_message = await BOT.send_message(
        #     chat_id=ADMINGROUP_ID,
        #     text="⏱️ <b>Запуск бота:</b> Начинаем."
        # )
        await print_other("(V) Запуск бота: Соединение с Телеграмом установлено.")

        await create_database()
        DP.include_router(handlers_rt)


        await print_other("(V) Запуск бота: Успех.")
        # await BOT.edit_message_text(
        #     chat_id=ADMINGROUP_ID,
        #     message_id=start_message.message_id,
        #     text="✅ <b>Запуск бота:</b> Успех."
        # )
        await DP.start_polling(BOT)

    finally:
        await session.close()


if __name__ == "__main__":
    try:
        run(print_other(f"(+) Запуск бота: Начинаем."))
        run(main())

    except Exception as e:
        error = str(e)
        if "ClientConnectorError: Cannot connect to host" in error:
            error_part = error.split(" ")
            error_tags = f"HTTP, Клиент, {error_part[9]}, {error_part[10]}, {error_part[11]}"
            error = f"Не удалось подключится к Bot API Телеграма — {error_tags}"

        else:
            error = str(e)

        run(print_error(f"{error}."))