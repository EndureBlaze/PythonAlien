import pygame
from pygame.sprite import Sprite


class PythonAlien(Sprite):
    """垃圾 Python 外星人"""

    def __init__(self, ai_settings, screen):
        """初始化"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载图像
        self.image = pygame.image.load(ai_settings.python_alien_image_dir)
        self.rect = self.image.get_rect()

        # 初始化在屏幕的左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储位置
        self.x = float(self.rect.x)

    def blitme(self):
        """绘制 Python 外星人"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """向左或向右移动外星人"""
        self.x += (self.ai_settings.python_alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x
