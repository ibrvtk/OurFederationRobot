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
            async with db.execute("SELECT * FROM roleplays WHERE user_id = ?", (user_id,)) as cursor:
                user_data = await cursor.fetchone()
                return user_data

    except Exception as e:
        await print_error(f"databases/players/roleplays.py: read_by_user_id(): {e}.")
        return None

async def db_read_users():
    '''
    Чтение данных всех людей.  
    Возвращает в виде списка `users_data`.  
    Если данных нет, — возвращает `None`.
    '''
    try:
        async with connect(DB_PLAYERS_DB) as db:
            async with db.execute("SELECT * FROM roleplays") as cursor:
                users_data = await cursor.fetchall()
                return users_data

    except Exception as e:
        await print_error(f"databases/players/roleplays.py: read_users(): {e}.")
        return None


async def db_read_by_is_prisoner(is_prisoner: int):
    '''
    Чтение всех `user_id`, у которых is_prisoner равен искомому.  
    Возвращает в виде списка `users_id`.  
    Если данных нет, — возвращает `None`.
    '''
    try:
        async with connect(DB_PLAYERS_DB) as db:
            async with db.execute("SELECT user_id FROM roleplays WHERE is_prisoner = ?", (is_prisoner,)) as cursor:
                users_id = await cursor.fetchone()
                return users_id

    except Exception as e:
        await print_error(f"databases/players/roleplays.py: read_by_is_prisoner(): {e}.")
        return None

async def db_read_by_party_membership(party_membership: str):
    '''
    Чтение всех `user_id`, у которых party_membership равен искомому.  
    Возвращает в виде списка `users_id`.  
    Если данных нет, — возвращает `None`.
    '''
    try:
        async with connect(DB_PLAYERS_DB) as db:
            async with db.execute("SELECT user_id FROM roleplays WHERE party_membership = ?", (party_membership,)) as cursor:
                users_id = await cursor.fetchone()
                return users_id

    except Exception as e:
        await print_error(f"databases/players/roleplays.py: read_by_party_membership(): {e}.")
        return None


# U
async def db_update_is_prisoner(user_id: int, is_prisoner: int) -> None:
    '''Обновление статуса заключения.'''
    try:
        async with connect(DB_PLAYERS_DB) as db:
            await db.execute("""
                UPDATE roleplays
                SET is_prisoner = ?
                WHERE user_id = ?
            """, (is_prisoner, user_id))
            await db.commit()

    except Exception as e:
        await print_error(f"databases/players/roleplays.py: update_is_prisoner(): {e}.")

async def db_update_is_rebel(user_id: int, is_rebel: int) -> None:
    '''Обновление статуса мятежника.'''
    try:
        async with connect(DB_PLAYERS_DB) as db:
            await db.execute("""
                UPDATE roleplays
                SET is_rebel = ?
                WHERE user_id = ?
            """, (is_rebel, user_id))
            await db.commit()

    except Exception as e:
        await print_error(f"databases/players/roleplays.py: update_is_rebel(): {e}.")

async def db_update_is_military(user_id: int, is_military: int) -> None:
    '''Обновление статуса военного.'''
    try:
        async with connect(DB_PLAYERS_DB) as db:
            await db.execute("""
                UPDATE roleplays
                SET is_military = ?
                WHERE user_id = ?
            """, (is_military, user_id))
            await db.commit()

    except Exception as e:
        await print_error(f"databases/players/roleplays.py: update_is_military(): {e}.")

async def db_update_party_membership(user_id: int, party_membership: str) -> None:
    '''Обновление членства в партии.'''
    try:
        async with connect(DB_PLAYERS_DB) as db:
            await db.execute("""
                UPDATE roleplays
                SET party_membership = ?
                WHERE user_id = ?
            """, (party_membership, user_id))
            await db.commit()

    except Exception as e:
        await print_error(f"databases/players/roleplays.py: update_party_membership(): {e}.")

async def db_update_reputation(user_id: int, reputation: str) -> None:
    '''Обновление репутации.'''
    try:
        async with connect(DB_PLAYERS_DB) as db:
            await db.execute("""
                UPDATE roleplays
                SET reputation = ?
                WHERE user_id = ?
            """, (reputation, user_id))
            await db.commit()

    except Exception as e:
        await print_error(f"databases/players/roleplays.py: update_reputation(): {e}.")