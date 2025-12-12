# Первая практика работы с MySQL. Помогли гайды с ютуба.
# Код изначально был написан на pymysql, но был переписан на aiomysql.
# Некоторые моменты **подсказал** Gemini,
# но в основном я опирался на асинх. код моей SQLite БД players.

from config import (
    DB_CONNECTS_SQL,
    DB_CONNECTS_NAME as NAME,
    DB_CONNECTS_HOST as HOST,
    DB_CONNECTS_PORT as PORT,
    DB_CONNECTS_USER as USER,
    DB_CONNECTS_PASSWORD as PASSWORD
)
from functions import print_error

from aiomysql import connect, DictCursor, Error



async def db_get_connection() -> connect:
    return await connect(
        db=NAME,
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        connect_timeout=10,
        cursorclass=DictCursor
    )


async def db_create_database() -> None:
    connection = await db_get_connection()
    try:
        async with connection.cursor() as db:
            await db.execute("SHOW TABLES LIKE 'connects'")
            result = await db.fetchone()

            if not result:
                with open(DB_CONNECTS_SQL, 'r', encoding='utf-8') as file:
                    sql_script = file.read()
                await db.execute(sql_script)
                await connection.commit()
            else:
                pass

    except Exception as e:
        await print_error(f"databases/connects: create_database(): {e}.")
        await connection.rollback()

    finally:
        connection.close()
        await connection.ensure_closed()


async def db_create_user(user_id: int, minecraft_nickname: str, keyword: str) -> None:
    connection = await db_get_connection()
    try:
        async with connection.cursor() as db:
            await db.execute("""
                INSERT INTO connects 
                (user_id, minecraft_nickname, keyword) 
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                minecraft_nickname = VALUES(minecraft_nickname),
                keyword = VALUES(keyword)
            """, (user_id, minecraft_nickname, keyword))
            await connection.commit()

    except Error as e:
        await print_error(f"databases/connects: create_database(): {e}.")
        await connection.rollback()
        
    finally:
        connection.close()
        await connection.ensure_closed()

async def db_delete_user(user_id: int) -> None:
    connection = await db_get_connection()
    try:
        async with connection.cursor() as db:
            await db.execute("DELETE FROM connects WHERE user_id = %s", (user_id,))
            await connection.commit()

    except Error as e:
        await print_error(f"databases/connects: delete_user(): {e}.")
        await connection.rollback()

    finally:
        connection.close()
        await connection.ensure_closed()


async def db_read_user(user_id: int):
    connection = await db_get_connection()
    try:
        async with connection.cursor() as db:
            await db.execute("SELECT * FROM connects WHERE user_id = %s", (user_id,))
            user_data = await db.fetchone()
            return user_data

    except Error as e:
        await print_error(f"databases/connects: create_database(): {e}.")
        return None
        
    finally:
        connection.close()
        await connection.ensure_closed()