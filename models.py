from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Account:
    """游戏账号"""
    id: Optional[int]
    game_name: str
    game_server: str
    account_name: str
    remark: str
    refresh_hour: int
    refresh_minute: int
    remind_enabled: bool
    remind_hour: int
    remind_minute: int
    created_at: str

@dataclass
class Task:
    """每日任务"""
    id: Optional[int]
    account_id: int
    task_name: str
    description: str
    created_at: str

@dataclass
class CheckIn:
    """打卡记录"""
    id: Optional[int]
    task_id: int
    check_date: str
    note: str
    screenshot_path: str
    created_at: str
