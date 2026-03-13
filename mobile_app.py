#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""星誓诗笺 - 移动端版本"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.utils import platform
from datetime import datetime
import os

from database import Database
from models import Account, Task, CheckIn

# 设置窗口大小（仅用于桌面测试）
if platform not in ('android', 'ios'):
    Window.size = (360, 640)

class AccountListScreen(Screen):
    """账号列表界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题栏
        title_bar = BoxLayout(size_hint_y=0.1, spacing=10)
        title_bar.add_widget(Label(text='星誓诗笺', font_size='24sp', bold=True))
        refresh_btn = Button(text='刷新', size_hint_x=0.3)
        refresh_btn.bind(on_press=self.refresh_accounts)
        title_bar.add_widget(refresh_btn)
        self.layout.add_widget(title_bar)
        
        # 账号列表
        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.accounts_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.accounts_layout.bind(minimum_height=self.accounts_layout.setter('height'))
        self.scroll_view.add_widget(self.accounts_layout)
        self.layout.add_widget(self.scroll_view)
        
        # 底部按钮
        bottom_bar = BoxLayout(size_hint_y=0.1, spacing=10)
        add_btn = Button(text='添加账号')
        add_btn.bind(on_press=self.show_add_account)
        bottom_bar.add_widget(add_btn)
        self.layout.add_widget(bottom_bar)
        
        self.add_widget(self.layout)
        self.refresh_accounts()
    
    def refresh_accounts(self, *args):
        """刷新账号列表"""
        self.accounts_layout.clear_widgets()
        accounts = self.db.get_all_accounts()
        
        if not accounts:
            self.accounts_layout.add_widget(
                Label(text='暂无账号，点击下方添加', size_hint_y=None, height=50)
            )
            return
        
        for account in accounts:
            account_card = self.create_account_card(account)
            self.accounts_layout.add_widget(account_card)
    
    def create_account_card(self, account):
        """创建账号卡片"""
        card = BoxLayout(orientation='vertical', size_hint_y=None, height=120, padding=10)
        card.canvas.before.clear()
        
        # 账号信息
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
        info_layout.add_widget(Label(
            text=f'{account.game_name} - {account.server}',
            font_size='16sp', bold=True, halign='left'
        ))
        info_layout.add_widget(Label(
            text=f'账号: {account.account_name}',
            font_size='14sp', halign='left'
        ))
        if account.remark:
            info_layout.add_widget(Label(
                text=f'备注: {account.remark}',
                font_size='12sp', halign='left', color=(0.7, 0.7, 0.7, 1)
            ))
        
        # 按钮
        btn_layout = BoxLayout(orientation='vertical', size_hint_x=0.3, spacing=5)
        
        tasks_btn = Button(text='任务', size_hint_y=0.5)
        tasks_btn.bind(on_press=lambda x: self.show_tasks(account))
        btn_layout.add_widget(tasks_btn)
        
        checkin_btn = Button(text='打卡', size_hint_y=0.5)
        checkin_btn.bind(on_press=lambda x: self.show_checkin(account))
        btn_layout.add_widget(checkin_btn)
        
        main_layout = BoxLayout(orientation='horizontal')
        main_layout.add_widget(info_layout)
        main_layout.add_widget(btn_layout)
        
        card.add_widget(main_layout)
        return card
    
    def show_add_account(self, instance):
        """显示添加账号对话框"""
        self.manager.current = 'add_account'
    
    def show_tasks(self, account):
        """显示任务列表"""
        tasks_screen = self.manager.get_screen('tasks')
        tasks_screen.set_account(account)
        self.manager.current = 'tasks'
    
    def show_checkin(self, account):
        """显示打卡界面"""
        checkin_screen = self.manager.get_screen('checkin')
        checkin_screen.set_account(account)
        self.manager.current = 'checkin'


class AddAccountScreen(Screen):
    """添加账号界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 标题
        self.layout.add_widget(Label(
            text='添加账号', font_size='20sp', bold=True, size_hint_y=0.1
        ))
        
        # 表单
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.7)
        
        form_layout.add_widget(Label(text='游戏名称:'))
        self.game_input = TextInput(multiline=False)
        form_layout.add_widget(self.game_input)
        
        form_layout.add_widget(Label(text='服务器:'))
        self.server_input = TextInput(multiline=False)
        form_layout.add_widget(self.server_input)
        
        form_layout.add_widget(Label(text='账号名称:'))
        self.account_input = TextInput(multiline=False)
        form_layout.add_widget(self.account_input)
        
        form_layout.add_widget(Label(text='备注:'))
        self.remark_input = TextInput(multiline=False)
        form_layout.add_widget(self.remark_input)
        
        self.layout.add_widget(form_layout)
        
        # 按钮
        btn_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        
        save_btn = Button(text='保存')
        save_btn.bind(on_press=self.save_account)
        btn_layout.add_widget(save_btn)
        
        cancel_btn = Button(text='取消')
        cancel_btn.bind(on_press=self.go_back)
        btn_layout.add_widget(cancel_btn)
        
        self.layout.add_widget(btn_layout)
        self.add_widget(self.layout)
    
    def save_account(self, instance):
        """保存账号"""
        game_name = self.game_input.text.strip()
        server = self.server_input.text.strip()
        account_name = self.account_input.text.strip()
        remark = self.remark_input.text.strip()
        
        if not game_name or not account_name:
            self.show_message('错误', '游戏名称和账号名称不能为空')
            return
        
        account = Account(
            id=None,
            game_name=game_name,
            server=server,
            account_name=account_name,
            remark=remark,
            refresh_hour=4,
            refresh_minute=0,
            reminder_hour=20,
            reminder_minute=0
        )
        
        self.db.add_account(account)
        self.show_message('成功', '账号添加成功')
        self.clear_form()
        self.go_back()
    
    def clear_form(self):
        """清空表单"""
        self.game_input.text = ''
        self.server_input.text = ''
        self.account_input.text = ''
        self.remark_input.text = ''
    
    def go_back(self, *args):
        """返回"""
        self.manager.get_screen('accounts').refresh_accounts()
        self.manager.current = 'accounts'
    
    def show_message(self, title, message):
        """显示消息"""
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.3)
        )
        popup.open()


class TasksScreen(Screen):
    """任务列表界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.current_account = None
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题栏
        title_bar = BoxLayout(size_hint_y=0.1, spacing=10)
        back_btn = Button(text='返回', size_hint_x=0.3)
        back_btn.bind(on_press=self.go_back)
        title_bar.add_widget(back_btn)
        
        self.title_label = Label(text='任务列表', font_size='20sp', bold=True)
        title_bar.add_widget(self.title_label)
        
        add_btn = Button(text='添加', size_hint_x=0.3)
        add_btn.bind(on_press=self.show_add_task)
        title_bar.add_widget(add_btn)
        
        self.layout.add_widget(title_bar)
        
        # 任务列表
        self.scroll_view = ScrollView(size_hint=(1, 0.9))
        self.tasks_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))
        self.scroll_view.add_widget(self.tasks_layout)
        self.layout.add_widget(self.scroll_view)
        
        self.add_widget(self.layout)
    
    def set_account(self, account):
        """设置当前账号"""
        self.current_account = account
        self.title_label.text = f'{account.game_name} - 任务'
        self.refresh_tasks()
    
    def refresh_tasks(self):
        """刷新任务列表"""
        self.tasks_layout.clear_widgets()
        
        if not self.current_account:
            return
        
        tasks = self.db.get_tasks_by_account(self.current_account.id)
        
        if not tasks:
            self.tasks_layout.add_widget(
                Label(text='暂无任务，点击右上角添加', size_hint_y=None, height=50)
            )
            return
        
        for task in tasks:
            task_card = self.create_task_card(task)
            self.tasks_layout.add_widget(task_card)
    
    def create_task_card(self, task):
        """创建任务卡片"""
        card = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, padding=10, spacing=10)
        
        # 任务信息
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.8)
        info_layout.add_widget(Label(
            text=task.task_name,
            font_size='16sp', bold=True, halign='left'
        ))
        if task.description:
            info_layout.add_widget(Label(
                text=task.description,
                font_size='12sp', halign='left', color=(0.7, 0.7, 0.7, 1)
            ))
        
        # 完成状态
        status_text = '✓ 已完成' if task.completed else '○ 未完成'
        status_color = (0, 1, 0, 1) if task.completed else (1, 0, 0, 1)
        info_layout.add_widget(Label(
            text=status_text,
            font_size='14sp', halign='left', color=status_color
        ))
        
        card.add_widget(info_layout)
        
        # 删除按钮
        delete_btn = Button(text='删除', size_hint_x=0.2)
        delete_btn.bind(on_press=lambda x: self.delete_task(task))
        card.add_widget(delete_btn)
        
        return card
    
    def show_add_task(self, instance):
        """显示添加任务对话框"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        content.add_widget(Label(text='任务名称:'))
        task_name_input = TextInput(multiline=False)
        content.add_widget(task_name_input)
        
        content.add_widget(Label(text='任务描述:'))
        task_desc_input = TextInput(multiline=True, size_hint_y=2)
        content.add_widget(task_desc_input)
        
        btn_layout = BoxLayout(size_hint_y=0.3, spacing=10)
        
        popup = Popup(title='添加任务', content=content, size_hint=(0.9, 0.6))
        
        def save_task(instance):
            task_name = task_name_input.text.strip()
            description = task_desc_input.text.strip()
            
            if not task_name:
                return
            
            task = Task(
                id=None,
                account_id=self.current_account.id,
                task_name=task_name,
                description=description,
                completed=False
            )
            
            self.db.add_task(task)
            self.refresh_tasks()
            popup.dismiss()
        
        save_btn = Button(text='保存')
        save_btn.bind(on_press=save_task)
        btn_layout.add_widget(save_btn)
        
        cancel_btn = Button(text='取消')
        cancel_btn.bind(on_press=popup.dismiss)
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(btn_layout)
        popup.open()
    
    def delete_task(self, task):
        """删除任务"""
        self.db.delete_task(task.id)
        self.refresh_tasks()
    
    def go_back(self, *args):
        """返回"""
        self.manager.current = 'accounts'


class CheckInScreen(Screen):
    """打卡界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.current_account = None
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题栏
        title_bar = BoxLayout(size_hint_y=0.1, spacing=10)
        back_btn = Button(text='返回', size_hint_x=0.3)
        back_btn.bind(on_press=self.go_back)
        title_bar.add_widget(back_btn)
        
        self.title_label = Label(text='打卡', font_size='20sp', bold=True)
        title_bar.add_widget(self.title_label)
        
        self.layout.add_widget(title_bar)
        
        # 任务列表
        self.scroll_view = ScrollView(size_hint=(1, 0.7))
        self.tasks_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))
        self.scroll_view.add_widget(self.tasks_layout)
        self.layout.add_widget(self.scroll_view)
        
        # 打卡按钮
        checkin_btn = Button(text='确认打卡', size_hint_y=0.2, font_size='18sp')
        checkin_btn.bind(on_press=self.do_checkin)
        self.layout.add_widget(checkin_btn)
        
        self.add_widget(self.layout)
        self.selected_tasks = []
    
    def set_account(self, account):
        """设置当前账号"""
        self.current_account = account
        self.title_label.text = f'{account.game_name} - 打卡'
        self.refresh_tasks()
    
    def refresh_tasks(self):
        """刷新任务列表"""
        self.tasks_layout.clear_widgets()
        self.selected_tasks = []
        
        if not self.current_account:
            return
        
        tasks = self.db.get_tasks_by_account(self.current_account.id)
        
        if not tasks:
            self.tasks_layout.add_widget(
                Label(text='暂无任务', size_hint_y=None, height=50)
            )
            return
        
        for task in tasks:
            if not task.completed:
                task_item = self.create_task_item(task)
                self.tasks_layout.add_widget(task_item)
    
    def create_task_item(self, task):
        """创建任务选项"""
        item = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, padding=5)
        
        checkbox = CheckBox(size_hint_x=0.2)
        checkbox.bind(active=lambda cb, value: self.toggle_task(task, value))
        item.add_widget(checkbox)
        
        label = Label(text=task.task_name, font_size='16sp', halign='left')
        item.add_widget(label)
        
        return item
    
    def toggle_task(self, task, selected):
        """切换任务选择"""
        if selected:
            if task not in self.selected_tasks:
                self.selected_tasks.append(task)
        else:
            if task in self.selected_tasks:
                self.selected_tasks.remove(task)
    
    def do_checkin(self, instance):
        """执行打卡"""
        if not self.selected_tasks:
            self.show_message('提示', '请选择要打卡的任务')
            return
        
        checkin_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for task in self.selected_tasks:
            # 标记任务完成
            self.db.update_task_status(task.id, True)
            
            # 记录打卡
            checkin = CheckIn(
                id=None,
                account_id=self.current_account.id,
                task_id=task.id,
                checkin_time=checkin_time,
                screenshot_path=None
            )
            self.db.add_checkin(checkin)
        
        self.show_message('成功', f'已完成 {len(self.selected_tasks)} 个任务的打卡')
        self.go_back()
    
    def go_back(self, *args):
        """返回"""
        self.manager.current = 'accounts'
    
    def show_message(self, title, message):
        """显示消息"""
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.3)
        )
        popup.open()


class StarVowPoemApp(App):
    """星誓诗笺应用"""
    
    def build(self):
        # 创建屏幕管理器
        sm = ScreenManager()
        
        # 添加各个界面
        sm.add_widget(AccountListScreen(name='accounts'))
        sm.add_widget(AddAccountScreen(name='add_account'))
        sm.add_widget(TasksScreen(name='tasks'))
        sm.add_widget(CheckInScreen(name='checkin'))
        
        return sm


if __name__ == '__main__':
    StarVowPoemApp().run()
