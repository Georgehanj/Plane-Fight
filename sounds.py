import pygame
from pygame import mixer
from threading import Thread

def play_sound_init():
	mixer.init()

def play_sound_explosion():
	sound_explosion = mixer.Sound('sounds/explosion.wav')
	sound_explosion.play()
	# while pygame.mixer.get_busy():
	# 	pass
		# pygame.time.wait(1000)
	# mixer.quit()

def play_sounds_quit():
	mixer.quit()

def play_sounds_bgm():
	sound_bgm = pygame.mixer.Sound("sounds/bgm.mp3")
	sound_bgm.play()

def thread_bgm():
	thread_bgm = Thread(target=play_sounds_bgm)
	thread_bgm.start()

