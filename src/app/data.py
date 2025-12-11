from aiogram.fsm.state import State, StatesGroup

from datetime import datetime
from dataclasses import dataclass



class ProfileConnect(StatesGroup):
    minecraft_nickname = State()

@dataclass
class ConnectDataclass:
    user_id: int
    minecraft_nickname: str

connect_data = {}


@dataclass
class ReputationDataclass:
    user_id: int
    reputation_id: int
    chat_id: int
    profile_message_id: int
    profile_message_text: str

reputation_data = {}


@dataclass
class ReportDataclass:
    report_id: datetime
    user_id: int
    target_id: int
    user_message_id: int
    target_message_id: int
    reply_message_id: int
    send_message_id: int
    report_reason: str
    is_from_group: bool
    chat_id: int

report_data = {}