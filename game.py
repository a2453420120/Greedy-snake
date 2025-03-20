import os
import random
from ui import *
from snake import *
import datetime

# 新增全局变量初始化
final_game_time = 0
music_volume = 0.5  # 初始音量，范围 0.0 - 1.0
music_playing = True  # 标记音乐是否正在播放

os.environ['PYGAME_DISABLE_RUNNABLE'] = '1'  # 新增在文件开头
# 在文件顶部添加全局变量（约第11行）
game_time_records = []

# 在游戏初始化部分添加音乐设置（约第17行）
def gameLoop():
    global final_game_time, paused  # 新增：声明 paused 为全局变量
    global game_time_records
    global final_game_time, music_volume, music_playing
    # 初始化pygame
    dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))

    # 初始化游戏状态
    game_start = True
    paused = False  # 新增：初始化 paused 变量

    # 游戏开始界面
    while game_start:
        dis.fill(WHITE)
        draw_message("贪吃蛇游戏", BLACK, dis, DIS_WIDTH/2-100, DIS_HEIGHT/3)
        # # 创建按钮矩形并绘制按钮
        start_btn_rect = pygame.Rect(DIS_WIDTH/2-75, DIS_HEIGHT/2, 150, 50)
        draw_button("开始游戏", start_btn_rect.x, start_btn_rect.y, start_btn_rect.width, start_btn_rect.height, BLACK, dis)
        #
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn_rect.collidepoint(event.pos):  # 使用手动创建的矩形对象
                    game_start =  not game_start



    # 在初始化pygame之后添加音乐加载代码
    pygame.mixer.init(frequency=44100, size=-16, channels=2)  # 添加音频参数
    pygame.mixer.music.set_volume(0.1)  # 设置音量

    try:
        pygame.mixer.music.load("音乐/周杰伦 - 迷魂曲.flac")
        pygame.mixer.music.play(-1, start=0.0)  # 确保从开头循环播放
    except pygame.error as e:
        print(f"音乐加载失败: {str(e)}")


    # 创建时钟对象用于控制游戏帧率（后续会用 clock.tick() 控制刷新速度）
    clock = pygame.time.Clock()

    game_over = False
    game_close = False
    start_time = pygame.time.get_ticks()
    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2
    #
    snake_List = []
    Length_of_snake = 1

    def generate_food_position():
       while True:
             foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
             foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
             if [foodx, foody] not in snake_List:
                 return foodx, foody
    #
    foodx, foody = generate_food_position()
    #
    x1_change = SNAKE_BLOCK
    y1_change = 0

    # 在游戏主循环的绘制部分添加（约第175行）
    while not game_over:
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
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                # 音量控制
                elif event.key == pygame.K_m:  # 静音/取消静音
                    music_playing = not music_playing
                    if music_playing:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                # 在键盘事件处理部分添加（约第95行）
                if event.type == pygame.KEYDOWN:
                    # 原有方向控制代码...
                    if event.key == pygame.K_l:  # K键减小音量
                        current_volume = max(0.0, pygame.mixer.music.get_volume() - 0.1)
                        pygame.mixer.music.set_volume(current_volume)
                    elif event.key == pygame.K_k:  # L键增大音量
                        current_volume = min(1.0, pygame.mixer.music.get_volume() + 0.1)
                        pygame.mixer.music.set_volume(current_volume)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # 暂停/继续按钮位置（左下角）
                button_width = 150
                button_height = 50
                button_x = 20
                button_y = DIS_HEIGHT - button_height - 20
                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                if button_rect.collidepoint(mouse_pos):
                    paused = not paused
        # shi
        if not paused:
            if x1 >= DIS_WIDTH:
                x1 = 0
            elif x1 < 0:
                x1 = DIS_WIDTH - SNAKE_BLOCK
            if y1 >= DIS_HEIGHT:
                y1 = 0
            elif y1 < 0:
                y1 = DIS_HEIGHT - SNAKE_BLOCK

            x1 += x1_change
            y1 += y1_change
            # 隐藏
            dis.fill(WHITE)
            # 画球 制造头
            pygame.draw.rect(dis, BLACK, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
            # 制造头
            snake_Head = [x1, y1]
            snake_List.append(snake_Head)
            # 去wei
            if len(snake_List) > Length_of_snake:
                del snake_List[0]
            # 死亡
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True
                    final_game_time = (pygame.time.get_ticks() - start_time) // 1000
                    game_time_records.append(final_game_time)
                    game_time_records = game_time_records[-10:]
            # 绘制yi
            draw_snake(SNAKE_BLOCK, snake_List, dis)
            # 分数
            draw_score(Length_of_snake - 1, dis)

            # 吃球
            if x1 == foodx and y1 == foody:
                 foodx, foody = generate_food_position()
                 Length_of_snake += 10

            current_real_time = datetime.datetime.now().strftime("%H:%M:%S")
            draw_message(f"现实时间: {current_real_time}", BLACK, dis, DIS_WIDTH - 200, DIS_HEIGHT - 50, center=True)

            current_game_time = (pygame.time.get_ticks() - start_time) // 1000
            draw_message(f"游戏时间: {current_game_time}", BLACK, dis, DIS_WIDTH - 200, DIS_HEIGHT - 80, center=True)

            # 显示音量
            draw_message(f"音量: {int(pygame.mixer.music.get_volume() * 100)}%", BLACK, dis, 10, 40)
            # 开始游戏
            pygame.display.update()
            if not paused:
                clock.tick(SNAKE_SPEED)

        while game_close:
            dis.fill(WHITE)
            y_position = DIS_HEIGHT/3
            draw_message("Game Over!", RED, dis, DIS_WIDTH/6, y_position)
            draw_message(f"游戏时间: {final_game_time}秒", RED, dis, DIS_WIDTH/6, y_position + 40)

            record_y = y_position + 100
            for i, record in enumerate(reversed(game_time_records)):
                draw_message(f"第 {len(game_time_records) - i} 次游戏时间: {record} 秒", RED, dis, DIS_WIDTH/6, record_y)
                record_y += 30

            button_width = 150
            button_height = 50
            button_margin = 20
            continue_button_x = DIS_WIDTH - button_width - button_margin
            continue_button_y = DIS_HEIGHT - button_height * 2 - button_margin * 1.5
            exit_button_x = DIS_WIDTH - button_width - button_margin
            exit_button_y = DIS_HEIGHT - button_height - button_margin

            draw_button("继续游戏", continue_button_x, continue_button_y, button_width, button_height, BLACK, dis)
            draw_button("退出游戏", exit_button_x, exit_button_y, button_width, button_height, BLACK, dis)



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    handle_exit_action()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    continue_button_rect = pygame.Rect(continue_button_x, continue_button_y, button_width, button_height)
                    if continue_button_rect.collidepoint(mouse_pos):
                        game_close = False
                        x1 = DIS_WIDTH / 2
                        y1 = DIS_HEIGHT / 2
                        x1_change = SNAKE_BLOCK
                        y1_change = 0
                        snake_List = []
                        Length_of_snake = 1
                        foodx, foody = generate_food_position()
                        start_time = pygame.time.get_ticks()
                        game_over = False
                        dis.fill(WHITE)
                    exit_button_rect = pygame.Rect(exit_button_x, exit_button_y, button_width, button_height)
                    if exit_button_rect.collidepoint(mouse_pos):
                        handle_exit_action()

            pygame.display.update()



# 退出处理方法
def handle_exit_action():
    pygame.mixer.music.stop()  # 停止音乐播放
    pygame.quit()
    quit()