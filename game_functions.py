import sys

import pygame
from bullet import Bullet
from python_alien import PythonAlien
from time import sleep


def check_keydown_events(
    event, stats, sb, ai_settings, screen,
        play_btn, python_aliens, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moveing_right = True
    elif event.key == pygame.K_LEFT:
        ship.moveing_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        start_game(
            ai_settings, screen, stats, sb,
            play_btn, ship, python_aliens, bullets)


def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moveing_right = False
    elif event.key == pygame.K_LEFT:
        ship.moveing_left = False


def check_events(
        ai_settings, screen, stats, sb,
        play_btn, ship, python_aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(
                event, stats, sb, ai_settings,
                screen, play_btn, python_aliens, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_btn(
                ai_settings, screen, stats, sb, play_btn,
                ship, python_aliens, bullets, mouse_x, mouse_y)


def check_play_btn(
        ai_settings, screen, stats, sb,
        play_btn, ship, python_aliens, bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    btn = play_btn.rect.collidepoint(mouse_x, mouse_y)
    if btn and not stats.game_active:
        start_game(
            ai_settings, screen, stats, sb,
            play_btn, ship, python_aliens, bullets)


def start_game(
        ai_settings, screen, stats, sb, play_btn, ship, python_aliens, bullets):
    """开始游戏的方法"""
    # 重置游戏设置
    ai_settings.initialize_dynamic_settings()

    # 隐藏光标
    pygame.mouse.set_visible(False)

    # 重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True

    # 重置记分牌图像
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # 清空外星人列表和子弹列表
    python_aliens.empty()
    bullets.empty()

    # 创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings, screen, ship, python_aliens)
    ship.center_ship()


def fire_bullet(ai_settings, screen, ship, bullets):
    """二营长方法"""
    # 二营长，开炮！
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_screen(
        ai_settings, screen, stats, sb, ship, python_alien, bullets, play_btn):
    """刷新屏幕"""
    # 改变颜色
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    python_alien.draw(screen)

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_btn.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(
        ai_settings, screen, stats, sb, ship, python_aliens, bullets):
    """更新子弹位置，并删除已消失子弹"""
    # 更新子单位置
    bullets.update()

    # 删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(
        ai_settings, screen, stats, sb, ship, python_aliens, bullets)


def check_bullet_alien_collisions(
        ai_settings, screen, stats, sb, ship, python_aliens, bullets):
    # 检查是否有子弹击中了外星人
    collisions = pygame.sprite.groupcollide(bullets, python_aliens, True, True)

    if collisions:
        for python_aliens in collisions.values():
            stats.score += ai_settings.python_alien_points * \
                len(python_aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(python_aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        # 提高等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, python_aliens)


def get_number_python_alien_x(ai_settings, python_alien_width):
    """计算每行可以放多少外星人"""
    available_space_x = ai_settings.screen_width - 2 * python_alien_width
    number_python_aliens_x = int(available_space_x / (2 * python_alien_width))
    return number_python_aliens_x


def get_number_python_alien_rows(
        ai_settings, ship_height, python_alien_height):
    """计算总共可以容纳多少"""
    available_space_y = (ai_settings.screen_height -
                         (3 * python_alien_height) - ship_height)
    number_rows = int(available_space_y / (3*python_alien_height))
    return number_rows


def create_python_alien(ai_settings, screen, python_aliens,
                        python_alien_number, row_number):
    """创建一行 Python 外星人"""
    python_alien = PythonAlien(ai_settings, screen)
    python_alien_width = python_alien.rect.width

    python_alien.x = python_alien_width + 2 * \
        python_alien_width * python_alien_number

    python_alien.rect.x = python_alien.x
    python_alien.rect.y = python_alien.rect.height + \
        2*python_alien.rect.height*row_number

    python_aliens.add(python_alien)


def create_fleet(ai_settings, screen, ship, python_aliens):
    """创建一组 Python 外星人"""
    python_alien = PythonAlien(ai_settings, screen)
    number_python_aliens_x = get_number_python_alien_x(
        ai_settings, python_alien.rect.width)
    number_rows = get_number_python_alien_rows(
        ai_settings, ship.rect.height, python_alien.rect.height)

    # 创建第一行外星人
    for row_number in range(number_rows):
        for python_alien_number in range(number_python_aliens_x):
            create_python_alien(ai_settings, screen,
                                python_aliens, python_alien_number, row_number)


def check_fleet_edges(ai_settings, python_aliens):
    """有外星人到达边缘时采取相应的措施"""
    for python_alien in python_aliens.sprites():
        if python_alien.check_edges():
            change_fleet_direction(ai_settings, python_aliens)
            break


def change_fleet_direction(ai_settings, python_aliens):
    """将整群外星人下移，并改变它们的方向"""
    for python_alien in python_aliens.sprites():
        python_alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, sb, screen, ship, python_aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将ships_left减1
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        python_aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, python_aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(
        ai_settings, stats, sb, screen, ship, python_aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for python_alien in python_aliens.sprites():
        if python_alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(
                ai_settings, stats, sb, screen,
                ship, python_aliens, bullets)
            break


def update_python_aliens(
        ai_settings, stats, sb, screen, ship, python_aliens, bullets):
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    check_fleet_edges(ai_settings, python_aliens)
    python_aliens.update()
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, sb, screen,
                        ship, python_aliens, bullets)

    if pygame.sprite.spritecollideany(ship, python_aliens):
        print("你挂了")
        ship_hit(ai_settings, stats, sb, screen, ship, python_aliens, bullets)


def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
