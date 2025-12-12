from aiogram import Dispatcher

from config import (
    BOT,
    ADMINGROUP_ID
)
from functions import print_error, print_other

from app.handlers import rt as handlers_rt
from app.callbacks import rt as callbacks_rt

from databases.players import db_create_database as db_players_create_database
from databases.connects import db_create_database as db_connects_create_database

from asyncio import run#, create_task
from aiohttp import ClientSession


DP = Dispatcher()



async def main() -> None:
    '''Запуск бота.'''
    session = ClientSession()

    try:
        await db_players_create_database()
        await db_connects_create_database()
        DP.include_router(handlers_rt)
        DP.include_router(callbacks_rt)
        await print_other("(i) (2/4) Запуск бота: Все БД в порядке, роутеры подключены.")

        start_message = await BOT.send_message(
            chat_id=ADMINGROUP_ID,
            text="✅"
        )
        await BOT.delete_message(ADMINGROUP_ID, start_message.message_id)
        await print_other("(i) (3/4) Запуск бота: Успешное соединение с Телеграмом.")

        await print_other("(V) (4/4) Запуск бота: Успех.")
        await DP.start_polling(BOT)

    finally:
        await session.close()


if __name__ == "__main__":
    try:
        run(print_other(f"(+) (1/4) Запуск бота: Начинаем."))
        run(main())

    except Exception as e:
        run(print_error(f"{str(e)}."))