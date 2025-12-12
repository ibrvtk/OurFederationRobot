from aiogram.fsm.state import State, StatesGroup

from datetime import datetime
from dataclasses import dataclass



class ProfileConnect(StatesGroup):
    minecraft_nickname = State()

@dataclass
class ConnectDataclass:
    '''
    *Датакласс для `callbacks.py`: `cb_profile_connect()`.*
    Нужен для передачи `minecraft_nickname` из FSM `ProfileConnect` в коллбэк.
    '''
    user_id: int
    minecraft_nickname: str

connect_data = {}


@dataclass
class ReputationDataclass:
    '''
    *Датакласс для `callbacks.py`: `cb_profile_*rep()`.*
    Нужен для чтения репутации. `reputation_id` — для игнорирования старых вызовов.
    TG-ID сообщений и чата хранятся для их динамичного редактирования, при нажатии на кнопки.
    '''
    user_id: int
    reputation_id: datetime
    chat_id: int
    profile_message_id: int
    profile_message_text: str

reputation_data = {}


@dataclass
class ReportDataclass:
    '''
    *Датакласс для `callbacks.py`: `cb_report_*()`.*
    Нужен для управления жалобой.
    TG-ID сообщений и чата хранятся для их динамичного редактирования, при нажатии на кнопки.
    '''
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