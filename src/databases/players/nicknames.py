from config import DB_PLAYERS_DB
from functions import print_error

from aiosqlite import connect



# R
async def db_read_by_user_id(user_id: int):
    '''
    Чтение всех данных человека, по его TG-ID.  
    Возвращает в виде списка `user_data`.  
    Если данных нет, — возвращает `None`.
    '''
    try:
        async with connect(DB_PLAYERS_DB) as db:
            async with db.execute("SELECT * FROM nicknames WHERE user_id = ?", (user_id,)) as cursor:
                user_data = await cursor.fetchone()
                return user_data

    except Exception as e:
        await print_error(f"databases/players/nicknames.py: read_by_user_id(): {e}.")
        return None

async def db_read_by_user_username(user_username: str):
    '''
    Чтение всех данных человека, по его @юзернейму.  
    Возвращает в виде списка `user_data`.  
    Если данных нет, — возвращает `None`.
    '''
    try:
        async with connect(DB_PLAYERS_DB) as db:
            async with db.execute("SELECT * FROM nicknames WHERE LOWER(user_username) = LOWER(?)", (user_username,)) as cursor:
                user_data = await cursor.fetchone()
                return user_data

    except Exception as e:
        await print_error(f"databases/players/nicknames.py: read_by_user_username(): {e}.")
        return None

async def db_read_by_minecraft_nickname(minecraft_nickname: str):
    '''
    Чтение всех данных человека, по его никнейму в майнкрафте.  
    Возвращает в виде списка `user_data`.  
    Если данных нет, — возвращает `None`.
    '''
    try:
        async with connect(DB_PLAYERS_DB) as db:
            async with db.execute("SELECT * FROM nicknames WHERE minecraft_nickname = ?", (minecraft_nickname,)) as cursor:
                user_data = await cursor.fetchone()
                return user_data

    except Exception as e:
        await print_error(f"databases/players/nicknames.py: read_by_minecraft_nickname(): {e}.")
        return None

async def db_read_user_id_by_minecraft_nickname(minecraft_nickname: str):
    '''
    Чтение TG-ID человека, по его никнейму в майнкрафте.  
    Возвращает в виде `result`.  
    Если данных нет, — возвращает `None`.
    '''
    try:
        async with connect(DB_PLAYERS_DB) as db:
            async with db.execute("SELECT user_id FROM nicknames WHERE minecraft_nickname = ?", (minecraft_nickname,)) as cursor:
                result = await cursor.fetchone()
                return result

    except Exception as e:
        await print_error(f"databases/players/nicknames.py: db_read_user_id_by_minecraft_nickname(): {e}.")
        return None

async def db_read_by_is_moderator(is_moderator: bool = True):
    '''
    Чтение данных всех модераторов.  
    Возвращает в виде списка `users_data`.  
    Если данных нет, — возвращает `None`.
    '''
    is_moderator = 1 if is_moderator else 0
    try:
        async with connect(DB_PLAYERS_DB) as db:
            async with db.execute("SELECT * FROM nicknames WHERE is_moderator = ?", (is_moderator,)) as cursor:
                users_data = await cursor.fetchone()
                return users_data

    except Exception as e:
        await print_error(f"databases/players/nicknames.py: read_by_is_moderator(): {e}.")
        return None

async def db_read_users():
    '''
    Чтение данных всех людей.  
    Возвращает в виде списка `users_data`.  
    Если данных нет, — возвращает `None`.
    '''
    try:
        async with connect(DB_PLAYERS_DB) as db:
            async with db.execute("SELECT * FROM nicknames") as cursor:
                users_data = await cursor.fetchall()
                return users_data

    except Exception as e:
        await print_error(f"databases/players/nicknames.py: read_users(): {e}.")
        return None


# U
async def db_update_minecraft_nickname(user_id: int, minecraft_nickname: str) -> None:
    '''Обновление майнкрафт никнейма *(если человек его изменил)*.'''
    user_data = await db_read_by_user_id(user_id)
    nickname_changes_count = user_data[4] + 1

    try:
        async with connect(DB_PLAYERS_DB) as db:
            await db.execute("""
                UPDATE nicknames
                SET minecraft_nickname = ?, nickname_changes_count = ?
                WHERE user_id = ?
            """, (minecraft_nickname, nickname_changes_count, user_id))
            await db.commit()

    except Exception as e:
        await print_error(f"databases/players/nicknames.py: update_minecraft_nickname(): {e}.")