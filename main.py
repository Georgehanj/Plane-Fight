a = int(1.5)
b = float(a)
b += 1.5
a = b

print(a)




def prep_ship(self):
	'''显示还剩下多少飞船'''
	self.ships = Group()
	for ship_number in range(self.stats.ships_left):
		ship = Ship(self.ai_settings, self.screen)
		ship.rect.x = 10 + ship_number * ship.rect.width
		ship.rect.y = 10
		self.ships.add(ship)