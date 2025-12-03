from config import BOT



async def get_user_user(user_id: int) -> str:
    '''
    Возвращает стандартизированный способ обращения к пользователю в сообщении:  
    "@username" если он есть, иначе "Имя (`TG-ID`)"
    '''
    user = await BOT.get_chat(user_id)
    user_user = f"@{user.username}" if user.username else f"{user.first_name} (<code>{user.id}</code>)"
    return user_user