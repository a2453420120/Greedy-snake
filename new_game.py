import pygame

# 假设这些常量已经在 constants.py 中定义，这里为了示例给出默认值
DIS_WIDTH = 800
DIS_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 模拟 draw_button 函数
def draw_button(text, x, y, width, height, color, surface):
    pygame.draw.rect(surface, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    surface.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)

def handle_exit_action():
    pygame.quit()
    quit()

def main():
    pygame.init()
    dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
    pygame.display.set_caption('带退出按钮的游戏示例')

    running = True
    while running:
        dis.fill(WHITE)

        # 绘制退出按钮
        exit_button_rect = draw_button("退出游戏", DIS_WIDTH/2 - 75, DIS_HEIGHT/2 + 60, 150, 50, BLACK, dis)

        pygame.display.update()

        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 handle_exit_action()
             elif event.type == pygame.MOUSEBUTTONDOWN:
                 mouse_pos = event.pos
                 if exit_button_rect.collidepoint(mouse_pos):
                     handle_exit_action()

if __name__ == "__main__":
    main()
