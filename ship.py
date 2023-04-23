import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

	def __init__(self, ai_settings, screen):
		super().__init__()
		# 初始化飞船并设置初始位置
		self.screen = screen
		self.ai_settings = ai_settings

		# 加载图片并获取其外形矩形
		self.image = pygame.image.load(r'images\ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		# 飞船放在屏幕底部中央
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom

		# 飞船的属性center中存储小数
		self.center = float(self.rect.centerx)

		# 移动标志
		self.moving_right = False
		self.moving_left = False

	def update(self):
		# 根据移动标志移动飞船位置
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor

		# 根据self.center更新rect对象
		self.rect.centerx = self.center

	def blitme(self):
		# 指定位置绘制飞船
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		'''让飞船在屏幕上居中'''
		self.center = self.screen_rect.centerx