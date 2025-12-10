from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from os import getenv
from dotenv import load_dotenv; load_dotenv()



BOT_TOKEN=getenv('BOT_TOKEN')
BOT=Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
FCMD_PREFIX=getenv('FCMD_PREFIX')

DEVELOPER_ID=getenv('DEVELOPER_ID')
SUPERADMINS_RAW = getenv('SUPERADMINS_ID')
SUPERADMINS_ID = []
for admin_id in SUPERADMINS_RAW.split(","):
    SUPERADMINS_ID.append(int(admin_id))
ADMINGROUP_ID=getenv('ADMINGROUP_ID')


DB_PLAYERS_DB=getenv('DB_PLAYERS_DB')
DB_PLAYERS_SQL=getenv('DB_PLAYERS_SQL')