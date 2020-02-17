from settings import Setting
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

import game_functions as gf

import pygame
from pygame.sprite import Group


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Setting()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption(ai_settings.game_title)

    play_btn = Button(ai_settings, screen, ai_settings.play_btn_text)

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建子弹编组
    bullets = Group()
    # 创建一组 Python 外星人
    python_aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, python_aliens)

    # 创建统计信息
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 开始游戏的主循环
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_btn,
                        ship, python_aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(
                ai_settings, screen, stats, sb, ship, python_aliens, bullets)
            gf.update_python_aliens(
                ai_settings, stats, sb, screen, ship, python_aliens, bullets)

        gf.update_screen(
            ai_settings, screen, stats,
            sb, ship, python_aliens, bullets, play_btn)


run_game()
