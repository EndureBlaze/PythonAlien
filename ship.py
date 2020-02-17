import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """初始化飞船并设置初始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图片
        self.image = pygame.image.load(ai_settings.ship_image_dir)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)

        # 是否移动的标志
        self.moveing_right = False
        self.moveing_left = False

    def update(self):
        """根据移动标志调整位置"""
        if self.moveing_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moveing_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
