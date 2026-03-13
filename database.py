import sqlite3
from datetime import datetime
from typing import List, Optional
from models import Account, Task, CheckIn

class Database:
    def __init__(self, db_name: str = "game_tasks.db"):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        """初始化数据库表"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 账号表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_name TEXT NOT NULL,
                game_server TEXT,
                account_name TEXT NOT NULL,
                remark TEXT,
                refresh_hour INTEGER DEFAULT 5,
                refresh_minute INTEGER DEFAULT 0,
                remind_enabled INTEGER DEFAULT 0,
                remind_hour INTEGER DEFAULT 20,
                remind_minute INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        ''')
        
        # 任务表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                task_name TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (account_id) REFERENCES accounts (id)
            )
        ''')
        
        # 打卡记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                check_date TEXT NOT NULL,
                note TEXT,
                screenshot_path TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (task_id) REFERENCES tasks (id)
            )
        ''')
        
        conn.commit()
        conn.close()

    # 账号管理
    def add_account(self, game_name: str, game_server: str, account_name: str, remark: str = "", 
                    refresh_hour: int = 5, refresh_minute: int = 0,
                    remind_enabled: bool = False, remind_hour: int = 20, remind_minute: int = 0) -> int:
        """添加账号"""
        conn = self.get_connection()
        cursor = conn.cursor()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            """INSERT INTO accounts (game_name, game_server, account_name, remark, 
               refresh_hour, refresh_minute, remind_enabled, remind_hour, remind_minute, created_at) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (game_name, game_server, account_name, remark, 
             refresh_hour, refresh_minute, 1 if remind_enabled else 0, remind_hour, remind_minute, created_at)
        )
        conn.commit()
        account_id = cursor.lastrowid
        conn.close()
        return account_id
    
    def update_account(self, account_id: int, game_name: str, game_server: str, account_name: str, remark: str = "",
                      refresh_hour: int = 5, refresh_minute: int = 0,
                      remind_enabled: bool = False, remind_hour: int = 20, remind_minute: int = 0):
        """更新账号"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE accounts SET game_name = ?, game_server = ?, account_name = ?, remark = ?,
               refresh_hour = ?, refresh_minute = ?, remind_enabled = ?, remind_hour = ?, remind_minute = ?
               WHERE id = ?""",
            (game_name, game_server, account_name, remark,
             refresh_hour, refresh_minute, 1 if remind_enabled else 0, remind_hour, remind_minute, account_id)
        )
        conn.commit()
        conn.close()
    
    def get_all_accounts(self) -> List[Account]:
        """获取所有账号"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT id, game_name, game_server, account_name, remark, 
                         refresh_hour, refresh_minute, remind_enabled, remind_hour, remind_minute, created_at 
                         FROM accounts""")
        rows = cursor.fetchall()
        conn.close()
        return [Account(id=r[0], game_name=r[1], game_server=r[2] or "", account_name=r[3], remark=r[4] or "",
                       refresh_hour=r[5], refresh_minute=r[6], remind_enabled=bool(r[7]),
                       remind_hour=r[8], remind_minute=r[9], created_at=r[10]) for r in rows]
    
    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        """根据ID获取账号"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT id, game_name, game_server, account_name, remark,
                         refresh_hour, refresh_minute, remind_enabled, remind_hour, remind_minute, created_at
                         FROM accounts WHERE id = ?""", (account_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Account(id=row[0], game_name=row[1], game_server=row[2] or "", account_name=row[3], remark=row[4] or "",
                          refresh_hour=row[5], refresh_minute=row[6], remind_enabled=bool(row[7]),
                          remind_hour=row[8], remind_minute=row[9], created_at=row[10])
        return None
    
    def delete_account(self, account_id: int):
        """删除账号"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
        conn.commit()
        conn.close()
    
    # 任务管理
    def add_task(self, account_id: int, task_name: str, description: str = "") -> int:
        """添加任务"""
        conn = self.get_connection()
        cursor = conn.cursor()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO tasks (account_id, task_name, description, created_at) VALUES (?, ?, ?, ?)",
            (account_id, task_name, description, created_at)
        )
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return task_id
    
    def get_tasks_by_account(self, account_id: int) -> List[Task]:
        """获取账号的所有任务"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, account_id, task_name, description, created_at FROM tasks WHERE account_id = ?",
            (account_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [Task(id=r[0], account_id=r[1], task_name=r[2], description=r[3], created_at=r[4]) for r in rows]
    
    def delete_task(self, task_id: int):
        """删除任务"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
    
    def update_task(self, task_id: int, task_name: str, description: str = ""):
        """更新任务"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET task_name = ?, description = ? WHERE id = ?",
            (task_name, description, task_id)
        )
        conn.commit()
        conn.close()
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """根据ID获取任务"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, account_id, task_name, description, created_at FROM tasks WHERE id = ?",
            (task_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return Task(id=row[0], account_id=row[1], task_name=row[2], description=row[3] or "", created_at=row[4])
        return None
    
    # 打卡管理
    def add_checkin(self, task_id: int, note: str = "", screenshot_path: str = "") -> int:
        """添加打卡记录"""
        conn = self.get_connection()
        cursor = conn.cursor()
        check_date = datetime.now().strftime("%Y-%m-%d")
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO checkins (task_id, check_date, note, screenshot_path, created_at) VALUES (?, ?, ?, ?, ?)",
            (task_id, check_date, note, screenshot_path, created_at)
        )
        conn.commit()
        checkin_id = cursor.lastrowid
        conn.close()
        return checkin_id
    
    def get_checkins_by_task(self, task_id: int) -> List[CheckIn]:
        """获取任务的所有打卡记录"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, task_id, check_date, note, screenshot_path, created_at FROM checkins WHERE task_id = ? ORDER BY check_date DESC",
            (task_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [CheckIn(id=r[0], task_id=r[1], check_date=r[2], note=r[3] or "", screenshot_path=r[4] or "", created_at=r[5]) for r in rows]
    
    def is_checked_today(self, task_id: int) -> bool:
        """检查今天是否已打卡"""
        conn = self.get_connection()
        cursor = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "SELECT COUNT(*) FROM checkins WHERE task_id = ? AND check_date = ?",
            (task_id, today)
        )
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    
    def get_checkin_streak(self, task_id: int) -> int:
        """获取连续打卡天数"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT check_date FROM checkins WHERE task_id = ? ORDER BY check_date DESC",
            (task_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return 0
        
        from datetime import datetime, timedelta
        streak = 0
        expected_date = datetime.now().date()
        
        for row in rows:
            check_date = datetime.strptime(row[0], "%Y-%m-%d").date()
            if check_date == expected_date:
                streak += 1
                expected_date -= timedelta(days=1)
            else:
                break
        
        return streak
    
    def get_checkin_calendar(self, task_id: int, year: int, month: int) -> List[str]:
        """获取指定月份的打卡日期列表"""
        conn = self.get_connection()
        cursor = conn.cursor()
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"
        
        cursor.execute(
            "SELECT check_date FROM checkins WHERE task_id = ? AND check_date >= ? AND check_date < ? ORDER BY check_date",
            (task_id, start_date, end_date)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [row[0] for row in rows]

    # 配置管理
    def get_config(self, key: str, default: str = "") -> str:
        """获取配置"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 确保配置表存在
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        
        cursor.execute("SELECT value FROM config WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return row[0]
        return default
    
    def set_config(self, key: str, value: str):
        """设置配置"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 确保配置表存在
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        
        cursor.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", (key, value))
        conn.commit()
        conn.close()
