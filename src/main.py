from aiogram import Dispatcher

from config import BOT
from functions import print_error, print_other

from app.handlers import rt as handlers_rt
# from app.callbacks import rt as callbacks_rt

from databases.profiles import create_database as profiles_create_database

from asyncio import run#, create_task
from aiohttp import ClientSession


DP = Dispatcher()



async def main() -> None:
    '''Запуск бота.'''
    session = ClientSession()

    try:
        await profiles_create_database()
        DP.include_router(handlers_rt)

        await print_other("(V) Запуск бота: Успех.")
        await DP.start_polling(BOT)

    finally:
        await session.close()


if __name__ == "__main__":
    try:
        run(print_other(f"(+) Запуск бота: Начинаем."))
        run(main())

    except Exception as e:
        run(print_error(f"{str(e)}."))