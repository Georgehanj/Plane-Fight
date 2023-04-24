import pygame
from threading import Thread

# 初始化 Pygame 应用
pygame.init()
screen = pygame.display.set_mode((640, 480))

# 加载声音文件
sound = pygame.mixer.Sound("sounds/bgm.mp3")

# 播放声音的函数
def play_sound():
    sound.play()


# 创建一个线程，并在该线程中播放声音
thread = Thread(target=play_sound)
thread.start()

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新屏幕
    screen.fill((255, 255, 255))
    pygame.display.flip()

# 退出 Pygame 应用
pygame.quit()