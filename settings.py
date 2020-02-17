# -*- coding: utf-8 -*-


class Setting():
    """存储《炎忍大战外星人》的所有设置"""

    def __init__(self):
        """初始化游戏设置"""
        # 游戏名称
        self.game_title = "炎忍大战 Python 飞船"
        # 按钮文字
        self.play_btn_text = "Start"
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        # 背景颜色
        self.bg_color = (217, 234, 253)
        # 飞船设置
        self.ship_limit = 3
        # 子弹大小
        self.bullet_width = 3
        self.bullet_height = 15
        # 子弹颜色
        self.bullet_color = 60, 60, 60
        # 子弹最多同时出现数目
        self.bullets_allowed = 10
        # Python 外星人设置
        self.fleet_drop_speed = 10
        # 每个 Python 飞船分数
        self.python_alien_points = 50
        # 以什么样的倍率加快游戏节奏
        self.speedup_scale = 1.2
        # 外星人点数的提高速度
        self.score_scale = 1.5
        # 两个图片的路径
        self.ship_image_dir = 'C:/Users/nihao/Documents/dock_menu/code/python/alien_invasion/images/yanren.png'
        self.python_alien_image_dir = 'C:/Users/nihao/Documents/dock_menu/code/python/alien_invasion/images/python.png'

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        # 自己的飞船移动速度
        self.ship_speed_factor = 1.5
        # 子弹的速度
        self.bullet_speed_factor = 3
        # Python 移动的速度
        self.python_alien_speed_factor = 1
        # fleet_direction为1表示向右；为-1表示向左
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.python_alien_speed_factor *= self.speedup_scale

        self.python_alien_points = int(
            self.python_alien_points * self.score_scale)
        print(self.python_alien_points)
