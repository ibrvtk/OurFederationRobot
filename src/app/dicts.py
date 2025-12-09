from datetime import datetime
from dataclasses import dataclass



report_data = {}

@dataclass
class report_dataclass:
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