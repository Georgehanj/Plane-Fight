class GameStats():
	'''跟踪游戏的统计信息'''
	def __init__(self, ai_settings):
		'''初始化'''
		self.ai_settings = ai_settings
		self.reset_stats()
		# 开始游戏处于非活动状态
		self.game_active = False
		# 不重置最高得分
		self.high_score = 0

	def reset_stats(self):
		'''初始化游戏运行期间可能出现的变化'''
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
