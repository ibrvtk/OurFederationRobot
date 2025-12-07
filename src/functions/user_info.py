from config import BOT

from functions import print_error

from databases.profiles.nicknames import (
    read_by_user_username as profiles_nicknames_read_by_user_username,
    read_by_minecraft_nickname as profiles_nicknames_read_by_minecraft_nickname
)



async def get_user_id(identifier):
    '''
    Принимает `identifier` *(любое значение)* и, используя БД `profiles` таблицу `nicknames`,
    сначала пытается обработать его как @юзернейм (используя функцию `databases/profiles/nicknames.py: read_by_user_username()`),
    а если не находит, то как майнкрафт-никнейм (функция `databases/profiles/nicknames.py: read_by_minecraft_nickname()`).  
    Возвращает `user_id` (int).
    Если человека нет в БД или случилась ошибка — возвращает `None`.
    '''
    try:
        if str(identifier).startswith("@"):
            # @юзернейм.
            user_username = str(identifier).replace("@", "")
            user_data = await profiles_nicknames_read_by_user_username(user_username)

            if not user_data:
                return None

            user_id = int(user_data[0])

        else:
            # Майнкрафт-никнейм.
            user_data = await profiles_nicknames_read_by_minecraft_nickname(identifier)

            if not user_data:
                return None

            user_id = int(user_data[0])
    
        return user_id

    except Exception as e:
        await print_error(f"functions/user_info.py: get_user_id(): {e}.")
        return None

async def get_user_user(user_id: int) -> str:
    '''
    Возвращает стандартизированный способ обращения к пользователю в сообщении:  
    "@username" если он есть, иначе "Имя (`TG-ID`)".  
    Для получения информации о искомом пользователе (`username` либо `first_name`) используется метод `get_chat()`.
    Если получить информацию не вышло, возвращает "`TG-ID`".
    '''
    try:
        user = await BOT.get_chat(user_id)
        user_user = f"@{user.username}" if user.username else f"{user.first_name} (<code>{user.id}</code>)"
        return user_user

    except Exception as e:
        await print_error(f"functions/user_info.py: get_user_user(): {e}.")
        return f"<code>{user_id}</code>"


async def is_bot(user_id: int) -> bool:
    '''
    Проверка на то, является ли искомый пользователь ботом.  
    Принимает TG-ID. Возвращает `True` если да и `False` если нет.
    '''
    try:
        user = await BOT.get_chat(user_id)
        if user.username and user.active_usernames[0].lower().endswith("bot"):
            return True
        else:
            return False

    except Exception:
        return False