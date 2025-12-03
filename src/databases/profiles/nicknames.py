from config import DB_PROFILES_DB

from prints import print_error

from aiosqlite import connect



# R
async def read_by_user_id(user_id: int):
    '''
    Чтение всех данных человека, по его TG-ID.  
    Возвращает в виде списка `user_data`.  
    Если данных нет, — возвращает `None`.
    '''
    try:
        async with connect(DB_PROFILES_DB) as db:
            async with db.execute("SELECT * FROM nicknames WHERE user_id = ?", (user_id,)) as cursor:
                user_data = await cursor.fetchone()
                return user_data

    except Exception as e:
        await print_error(f"databases/players/nicknames.py: read_by_user_id(): {e}.")
        return None

async def read_by_user_username(user_username: str):
    '''
    Чтение всех данных человека, по его @юзернейму.  
    Возвращает в виде списка `user_data`.  
    Если данных нет, — возвращает `None`.
    '''
    try:
        async with connect(DB_PROFILES_DB) as db:
            async with db.execute("SELECT * FROM nicknames WHERE LOWER(user_username) = LOWER(?)", (user_username,)) as cursor:
                user_data = await cursor.fetchone()
                return user_data

    except Exception as e:
        await print_error(f"databases/players/nicknames.py: read_by_user_username(): {e}.")
        return None

async def read_by_minecraft_nickname(minecraft_nickname: str):
    '''
    Чтение всех данных человека, по его никнейму в майнкрафте.  
    Возвращает в виде списка `user_data`.  
    Если данных нет, — возвращает `None`.
    '''
    try:
        async with connect(DB_PROFILES_DB) as db:
            async with db.execute("SELECT * FROM nicknames WHERE minecraft_nickname = ?", (minecraft_nickname,)) as cursor:
                user_data = await cursor.fetchone()
                return user_data

    except Exception as e:
        await print_error(f"databases/players/nicknames.py: read_by_minecraft_nickname(): {e}.")
        return None
    
async def read_users():
    '''
    Чтение данных всех людей.  
    Возвращает в виде списка `users_data`.  
    Если данных нет, — возвращает `None`.
    '''
    try:
        async with connect(DB_PROFILES_DB) as db:
            async with db.execute("SELECT * FROM nicknames") as cursor:
                users_data = await cursor.fetchall()
                return users_data

    except Exception as e:
        await print_error(f"databases/players/nicknames.py: read_users(): {e}.")
        return None


# U
async def change_minecraft_nickname(user_id: int, minecraft_nickname: str) -> None:
    '''Обновление майнкрафт никнейма *(если человек его изменил)*.'''
    user_data = await read_by_user_id(user_id)
    nickname_changes_count = user_data[3] + 1

    try:
        async with connect(DB_PROFILES_DB) as db:
            await db.execute("""
                UPDATE nicknames 
                SET minecraft_nickname = ?, nickname_changes_count = ?
                WHERE user_id = ?
            """, (minecraft_nickname, nickname_changes_count, user_id))
            await db.commit()

    except Exception as e:
        await print_error(f"databases/players/nicknames.py: change_minecraft_nickname(): {e}.")