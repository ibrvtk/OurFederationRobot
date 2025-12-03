from config import DB_PROFILES_DB

from functions import print_error

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
            async with db.execute("SELECT * FROM donates WHERE user_id = ?", (user_id,)) as cursor:
                user_data = await cursor.fetchone()
                return user_data

    except Exception as e:
        await print_error(f"databases/profiles/donates.py: read_by_user_id(): {e}.")
        return None

async def read_users():
    '''
    Чтение данных всех людей.  
    Возвращает в виде списка `users_data`.  
    Если данных нет, — возвращает `None`.
    '''
    try:
        async with connect(DB_PROFILES_DB) as db:
            async with db.execute("SELECT * FROM donates") as cursor:
                users_data = await cursor.fetchall()
                return users_data

    except Exception as e:
        await print_error(f"databases/profiles/donates.py: read_users(): {e}.")
        return None


# U
async def update_balance(user_id: int, balance: int) -> None:
    '''Обновление баланса.'''
    user_data = await read_by_user_id(user_id)
    donate_count = user_data[4] + 1

    try:
        async with connect(DB_PROFILES_DB) as db:
            await db.execute("""
                UPDATE donates
                SET balance = ?, donate_count = ?
                WHERE user_id = ?
            """, (balance, donate_count, user_id))
            await db.commit()

    except Exception as e:
        await print_error(f"databases/profiles/donates.py: update_balance(): {e}.")

async def update_inventory(user_id: int, inventory: str) -> None:
    '''Обновление инвентаря.'''
    try:
        async with connect(DB_PROFILES_DB) as db:
            await db.execute("""
                UPDATE donates
                SET inventory = ?
                WHERE user_id = ?
            """, (inventory, user_id))
            await db.commit()

    except Exception as e:
        await print_error(f"databases/profiles/donates.py: update_inventory(): {e}.")

async def update_is_tradeban(user_id: int, is_tradeban: int) -> None:
    '''Обновление статуса блокировки торговли *(трейдбан)*.'''
    try:
        async with connect(DB_PROFILES_DB) as db:
            await db.execute("""
                UPDATE donates
                SET is_tradeban = ?
                WHERE user_id = ?
            """, (is_tradeban, user_id))
            await db.commit()

    except Exception as e:
        await print_error(f"databases/profiles/donates.py: update_is_tradeban(): {e}.")