import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import json
import sounds


def check_keydown_events(event, ai_settings, screen, ship, bullets, stats):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	if event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		record_high_score(stats)
		sounds.play_sounds_quit()
		sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
	# 创建一颗子弹，加入编组中
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)


def check_keyup_events(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	if event.key == pygame.K_LEFT:
		ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
	# 监控键盘鼠标
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets, stats)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
	'''玩家单击Play后开始新游戏'''
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		# 重置游戏难度
		ai_settings.initialize_dynamic_settings()
		# 隐藏光标
		pygame.mouse.set_visible(False)
		# 重置游戏信息
		stats.reset_stats()
		stats.game_active = True
		# 重置记分牌图像
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()

		# 初始声音
		sounds.play_sound_init()

		# 清空外星人和子弹
		aliens.empty()
		bullets.empty()

		# 创建新外星人，并让飞船在中间
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	# 更新子弹位置 并删除子弹
	bullets.update()

	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_bullet_alien_conllisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_conllisions(ai_settings,screen, stats, sb, ship, aliens, bullets):
	# 检查是否有子弹击中外星人，有的花就删除两者
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

	if collisions:
		# 播放爆炸声音
		sounds.play_sound_explosion()
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(collisions)
			sb.prep_score()
		check_high_score(stats, sb)

	if len(aliens) == 0:
		# 删除子弹并新建外星人,加快游戏节奏
		bullets.empty()
		ai_settings.increase_speed()
		# 提高等级
		stats.level += 1
		sb.prep_level()

		create_fleet(ai_settings, screen, ship, aliens)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	# 每次循环都重绘背景颜色
	screen.fill(ai_settings.bg_color)

	# 绘制子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()

	# 绘制飞机
	ship.blitme()
	aliens.draw(screen)

	# 显示得分
	sb.show_score()

	# 如果游戏处于非活动状态，绘制Play按钮
	if not stats.game_active:
		play_button.draw_button()

	# 让最近绘制的屏幕可见
	pygame.display.flip()


def create_fleet(ai_settings, screen, ship, aliens):
	# 创建外星人群
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)


	# 创建外星人群
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
	# 计算每行可容纳多少
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
	'''计算屏幕可容纳读诵好外星人'''
	available_apace_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(available_apace_y / (2 * alien_height))
	return number_rows


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
	'''更新外星人群位置'''
	check_fleet_edges(ai_settings, aliens)
	aliens.update()

	# 检查外星人和飞船是否发生碰撞
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

	# 检查外星人是否到达底部
	check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
	'''外星人达到边缘措施'''
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break


def change_fleet_direction(ai_settings, aliens):
	'''群向下移动，并且改变其方向'''
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
	'''响应被外星人撞到的飞船'''
	if stats.ships_left >0:
		# 将ship_left 减1
		stats.ships_left -= 1
		# 更新记分牌
		sb.prep_ships()

		# 清空飞船和子弹
		aliens.empty()
		bullets.empty()

		# 创建一群外星人并将飞船放到屏幕底部中央
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		# 暂停
		sleep(0.5)

	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
	'''检查是否有飞船到底部'''
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# 像飞船撞到一样处理
			ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
	"""检查是否有新的最高分"""
	if stats.score >stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()


def record_high_score(stats):
	'''添加最高分数到json文件'''
	with open(r'data\high_score.json') as file_object:
		json_data = json.load(file_object)
		if stats.score > json_data['high_score']:
			json_data['high_score'] = stats.score
			with open(r'data\high_score.json', 'w') as file_object2:
				json.dump(json_data, file_object2)