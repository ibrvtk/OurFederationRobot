from config import BOT
from functions import print_error

from databases.players.nicknames import (
    read_by_user_id as players_nicknames_read_by_user_id,
    read_by_user_username as players_nicknames_read_by_user_username,
    read_by_minecraft_nickname as players_nicknames_read_by_minecraft_nickname
)
from databases.players.roleplays import read_by_user_id as players_roleplays_read_by_user_id
from databases.players.donates import read_by_user_id as players_donates_read_by_user_id

from datetime import datetime



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
            user_data = await players_nicknames_read_by_user_username(user_username)

            if not user_data:
                return None

            user_id = int(user_data[0])

        else:
            # Майнкрафт-никнейм.
            user_data = await players_nicknames_read_by_minecraft_nickname(identifier)

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


async def get_reputation_as_list(
        user_id: int,
        return_int: bool = False, return_str: bool = False,
        return_with_user_id: int | None = None, return_without_user_id: int | None = None
        ):
    '''
    Получить репутацию в определённом виде:
    * По умолчанию просто вернёт список людей, которые дали репутацию `user_id`;
    * `return_int` — вернёт integer значение в кол-ве людей, которые находятся в списке;
    * `return_str` — вернёт string строку в формате `user_id,user_id,...`.
    * `return_with_user_id` — тоже возвращает список, но добавляет в него указанного человека.
    * `return_without_user_id` — то же, что и `return_with_user_id`, но возвращает список БЕЗ указанного человека.
    Не конфликтует со своим "братом" по функционалу.
    '''
    try:
        user_data = await players_roleplays_read_by_user_id(user_id)
        if not user_data or len(user_data) < 6:
            if return_int:
                return 0
            if return_str:
                return "None"
            return None

        reputation_str = str(user_data[5])

        if reputation_str == "None":
            if return_with_user_id is not None:
                # Если репутации нет, но нужно вернуть с пользователем из return_with_user_id.
                reputation_list = [return_with_user_id]

                if return_int:
                    return 1
                if return_str:
                    return str(return_with_user_id)
                return reputation_list

            if return_int:
                return 0
            if return_str:
                return "None"
            return []

        reputation_list = []
        for u_id_str in reputation_str.split(","):
            reputation_list.append(int(u_id_str))

        if return_with_user_id is not None and return_with_user_id not in reputation_list:
            # Возвращаем с пользователем из return_with_user_id.
            reputation_list.append(return_with_user_id)

        if return_without_user_id is not None:
            # Возвращаем без пользователя из return_without_user_id.
            reputation_list = [uid for uid in reputation_list if uid != return_without_user_id]

        if return_int:
            return len(reputation_list)
        if return_str:
            return ",".join(str(u_id) for u_id in reputation_list)
        
        return reputation_list

    except Exception as e:
        print_error(f"functions/user_info(): get_reputation_as_list: {e}.")
        if return_int:
            return 0
        return "None"


async def get_full_data(user_id: int, without_donate: bool = False):
    '''
    Получить все данные пользователя из всех таблиц БД `profiles`.
    * `without_donate` — не получать данные из таблицы `donates`?
    '''
    try:
        nicknames_data = await players_nicknames_read_by_user_id(user_id)
        if not nicknames_data:
            return None

        roleplays_data = await players_roleplays_read_by_user_id(user_id)
        donates_data = await players_donates_read_by_user_id(user_id)

        reputation = await get_reputation_as_list(user_id=user_id, return_int=True)
        user_user = await get_user_user(user_id)

        return {
            "user_id": user_id,
            "user_user": user_user,
            "nicknames": {
                "username": str(nicknames_data[1]),
                "minecraft_nickname": str(nicknames_data[2]),
                "registration_date": datetime.fromtimestamp(nicknames_data[3]).strftime("%d.%m.%Y %H:%M"),
                "nickname_changes_count": int(nicknames_data[4]),
            },
            "roleplays": {
                "is_prisoner": "Нет" if roleplays_data[1] == 0 else "Да",
                "is_rebel": "Нет" if roleplays_data[2] == 0 else "Да",
                "is_military": "Нет" if roleplays_data[3] == 0 else "Да",
                "party_membership": "Нигде не состоит" if roleplays_data[4] == "None" else f"{roleplays_data[4]}",
                "reputation": reputation,
            },
            "donates": {
                "balance": int(donates_data[1]),
                "inventory": str(donates_data[2]),
                "is_tradeban": "Нет" if roleplays_data[3] == 0 else "Да",
                "donate_count": int(donates_data[4]),
            } if not without_donate else None
        }

    except Exception as e:
        print_error(f"functions/user_info(): get_full_data: {e}.")
        return None