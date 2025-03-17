import os
import pygame
import random
from constants import *
from ui import *
from snake import *
# 在需要显示时间的位置添加（例如在游戏主循环中）
import datetime  # 添加在文件开头

from ui import init_font

# 新增全局变量初始化
final_game_time = 0

os.environ['PYGAME_DISABLE_RUNNABLE'] = '1'  # 新增在文件开头
def gameLoop():
    global final_game_time
    init_font()  # 确保在游戏循环开始前初始化字体
    # 初始化pygame
    pygame.init()
    dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
    pygame.display.set_caption('贪吃蛇游戏')
    clock = pygame.time.Clock()

    # 初始化游戏状态
    game_over = False
    game_start = True
    game_close = False
    start_time = pygame.time.get_ticks()  # 游戏开始时开始计时
    fast_time = 0  # 快速计时
    slow_time = 0  # 慢速计时

    # 游戏开始界面
    while game_start:
        dis.fill(WHITE)
        draw_message("贪吃蛇游戏", BLACK, dis, DIS_WIDTH/2-100, DIS_HEIGHT/3)  # 添加坐标
        draw_button("开始游戏", DIS_WIDTH/2-75, DIS_HEIGHT/2, 150, 50, BLACK, dis)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_start = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if DIS_WIDTH/2-75 <= mouse_pos[0] <= DIS_WIDTH/2+75 and \
                   DIS_HEIGHT/2 <= mouse_pos[1] <= DIS_HEIGHT/2+50:
                    game_start = False

    # 初始化蛇的位置和速度
    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2
    x1_change = 0
    y1_change = 0

    # 初始化蛇的列表和长度
    snake_List = []
    Length_of_snake = 1

    # 初始化食物位置
    def generate_food_position():
        while True:
            foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            # 检查食物是否在蛇身内部
            if [foodx, foody] not in snake_List:
                return foodx, foody

    foodx, foody = generate_food_position()

    # 直接开始移动
    x1_change = SNAKE_BLOCK
    y1_change = 0

    while not game_over:
        # 游戏主循环逻辑
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change <= 0:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change >= 0:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change <= 0:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change >= 0:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        # 检查是否出界
        if x1 >= DIS_WIDTH:
            x1 = 0
        elif x1 < 0:
            x1 = DIS_WIDTH - SNAKE_BLOCK
        if y1 >= DIS_HEIGHT:
            y1 = 0
        elif y1 < 0:
            y1 = DIS_HEIGHT - SNAKE_BLOCK

        # 更新蛇的位置
        x1 += x1_change
        y1 += y1_change

        # 绘制游戏界面
        dis.fill(WHITE)
        pygame.draw.rect(dis, BLACK, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

        # 更新蛇的身体
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 检查是否撞到自己
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
                final_game_time = (pygame.time.get_ticks() - start_time) // 1000  # 新增冻结时间

        # 游戏结束界面
        while game_close:
            dis.fill(WHITE)
            y_position = DIS_HEIGHT/3
            draw_message("Game Over!", RED, dis, DIS_WIDTH/6, y_position)
            draw_message(f"游戏时间: {final_game_time}秒", RED, dis, DIS_WIDTH/6, y_position+40)  # 使用冻结时间
            # 等动物死完了之后 这游戏时间停止进行

            draw_button("继续游戏", DIS_WIDTH/2-75, DIS_HEIGHT/2, 150, 50, BLACK, dis)
            # draw_button("退出游戏", DIS_WIDTH/2-75, DIS_HEIGHT/2+60, 150, 50, BLACK, dis)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 处理窗口关闭事件
                    game_over = True
                    game_close = False
                if event.type == pygame.MOUSEBUTTONDOWN:  # 处理鼠标点击事件
                    mouse_pos = pygame.mouse.get_pos()
                    # 检查是否点击在按钮的水平范围内（X轴）
                    if DIS_WIDTH/2-75 <= mouse_pos[0] <= DIS_WIDTH/2+75:
                        # 检查是否点击在"继续游戏"按钮的垂直范围内（Y轴）
                        if DIS_HEIGHT/2 <= mouse_pos[1] <= DIS_HEIGHT/2+50:
                            game_close = False  # 关闭结束界面
                            # 重置蛇的初始状态
                            x1 = DIS_WIDTH / 2  # 重置蛇头X坐标
                            y1 = DIS_HEIGHT / 2  # 重置蛇头Y坐标
                            x1_change = SNAKE_BLOCK  # 初始向右移动
                            y1_change = 0
                            snake_List = []  # 清空蛇身列表
                            Length_of_snake = 1  # 重置蛇长
                            foodx, foody = generate_food_position()  # 生成新食物
                            start_time = pygame.time.get_ticks()  # 重置计时器
                            # 重置速度计时
                            fast_time = 0
                            slow_time = 0
                            # 重置游戏状态
                            game_over = False
                            game_start = False
                            dis.fill(WHITE)  # 清空画布
                            pygame.display.update()  # 立即更新界面

        # 绘制蛇
        draw_snake(SNAKE_BLOCK, snake_List, dis)

        # 显示分数
        draw_score(Length_of_snake - 1, dis)

        # 检查是否吃到食物
        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food_position()
            Length_of_snake += 10

        # 更新计时
        if x1_change != 0 or y1_change != 0:
            if x1_change == SNAKE_BLOCK * 2 or y1_change == SNAKE_BLOCK * 2:  # 快速移动
                fast_time += 1



        # 显示现实时间
        current_real_time = datetime.datetime.now().strftime("%H:%M:%S")
        draw_message(f"现实时间: {current_real_time}", BLACK, dis, DIS_WIDTH - 200, DIS_HEIGHT - 50, center=True)

        # 显示游戏时间
        current_game_time = (pygame.time.get_ticks() - start_time) // 1000
        draw_message(f"游戏时间: {current_game_time}", BLACK, dis, DIS_WIDTH - 200, DIS_HEIGHT - 80, center=True)

        pygame.display.update()
        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()