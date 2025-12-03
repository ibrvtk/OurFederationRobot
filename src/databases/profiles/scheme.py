from config import (
    BOT,
    DB_PROFILES_DB, DB_PROFILES_SQL
)

from functions import print_error

from aiosqlite import connect
from datetime import datetime



async def create_database() -> None:
    '''
    ## Создание БД `profiles`
    Хранит в себе три таблицы: `nicknames`, `roleplays` и `donates`.

    ### `nicknames`

    * `minecraft_nickname` — никнейм в майнкрафте;
    * `registration_date` — дата, когда ТГ-аккаунт был привязан к никнейму *(то бишь дата начала игры на сервере)*;
    * `is_banned` — забанен ли человек.

    ### `roleplays`
    
    * `is_prisoner` — заключён ли в тюрьму;
    * `is_rebel` — восстал ли против **действующего** правительства;
    * `is_military` — является ли военным;
    * `party_membership` — название партии, в котором оформлено членство.

    ### `donates`
    
    * `balance` — донат баланс;
    * `inventory` — предметы в инвентаре *(через запятую)*;
    * `is_tradeban` — заблокирован ли доступ к рынку или аукциону;
    * `donate_count` — сколько раз донатил *(пополнял баланс, покупал предметы и так далее)*.
    '''
    try:
        async with connect(DB_PROFILES_DB) as db:
            with open(DB_PROFILES_SQL, 'r', encoding='utf-8') as file:
                sql_script = file.read()
            await db.executescript(sql_script)
            await db.commit()

    except Exception as e:
        await print_error(f"databases/profiles: createDatabase(): {e}.")


async def create_user(user_id: int, minecraft_nickname: str, registration_date: datetime) -> None:
    '''Добавление человека в БД.'''
    user = await BOT.get_chat(user_id)

    try:
        async with connect(DB_PROFILES_DB) as db:
            await db.execute("""
                INSERT OR IGNORE INTO nicknames 
                (user_id, user_username, minecraft_nickname, registration_date, nickname_changes_count)
                VALUES (?, ?, ?, ?, 0)
            """, (user_id, user.username, minecraft_nickname, registration_date,))

            await db.execute("""
                INSERT OR IGNORE INTO roleplays 
                (user_id, is_prisoner, is_rebel, is_military, party_membership)
                VALUES (?, 0, 0, 0, 'None')
            """, (user_id,))

            await db.execute("""
                INSERT OR IGNORE INTO donates 
                (user_id, balance, inventory, is_tradeban, donate_count)
                VALUES (?, 0, 'None', 0, 0)
            """, (user_id,))

            await db.commit()

    except Exception as e:
        await print_error(f"databases/players: create_user(): {e}.")

async def delete_user(user_id: int) -> None:
    '''Удаление человека из БД.'''
    try:
        async with connect(DB_PROFILES_DB) as db:
            await db.execute("DELETE FROM nicknames WHERE user_id = ?", (user_id,))
            await db.execute("DELETE FROM roleplays WHERE user_id = ?", (user_id,))
            await db.execute("DELETE FROM donates WHERE user_id = ?", (user_id,))
            await db.commit()

    except Exception as e:
        await print_error(f"databases/players: delete_user(): {e}.")