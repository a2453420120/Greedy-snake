# 启动游戏
import os
import pygame

# 必须在所有导入之前初始化pygame
pygame.init()

# 强制设置Python环境编码
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 假设 game.py 文件在当前目录下
from game import gameLoop
from constants import *

if __name__ == "__main__":
    while True:
        try:
            dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
            pygame.display.set_caption('贪吃蛇游戏')
            gameLoop()
        except KeyboardInterrupt:
            pygame.quit()
            break