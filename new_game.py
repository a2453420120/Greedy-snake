import pygame

# 初始化 Pygame
pygame.init()

# 设置窗口尺寸
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("关闭按钮示例")

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 当检测到 QUIT 事件时，将 running 标志设置为 False，退出主循环
            running = False

    # 更新屏幕显示
    pygame.display.flip()

# 退出 Pygame
pygame.quit()