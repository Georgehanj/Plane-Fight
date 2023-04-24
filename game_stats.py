import json

class GameStats():
	'''跟踪游戏的统计信息'''
	def __init__(self, ai_settings):
		'''初始化'''
		self.ai_settings = ai_settings
		self.reset_stats()
		# 开始游戏处于非活动状态
		self.game_active = False
		# 不重置最高得分
		with open(r'data\high_score.json') as file_object:
			json_data = json.load(file_object)
			self.high_score = json_data['high_score']


	def reset_stats(self):
		'''初始化游戏运行期间可能出现的变化'''
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
