import pygame
from constants import *

# 使用更可靠的中文字体路径（macOS Monterey及更新版本）
try:
    FONT_STYLE = pygame.font.Font("/System/Library/Fonts/Supplemental/STHeiti Medium.ttf", 25)
except:
    try:
        FONT_STYLE = pygame.font.Font("/System/Library/Fonts/STHeiti Medium.ttc", 25)
    except Exception as e:
        print(f"字体加载失败: {e}")
        FONT_STYLE = pygame.font.Font(None, 25)

def draw_message(msg, color, display, x, y, center=False):  # 添加 center 参数
    try:
        msg_str = str(msg).encode('utf-8').decode('utf-8')
        mesg = FONT_STYLE.render(msg_str, True, color)
        text_rect = mesg.get_rect()
        if center:  # 添加居中逻辑
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        display.blit(mesg, text_rect)
    except Exception as e:
        try:
            # Fallback to ASCII-only error display
            backup_font = pygame.font.SysFont("Arial", 25)
            display.blit(backup_font.render("ERROR", True, RED), [10, 10])
        except:
            # Ultimate fallback to prevent crash
            pass

def draw_button(text, x, y, width, height, color, display):
    pygame.draw.rect(display, color, [x, y, width, height])
    text_surf = FONT_STYLE.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + width/2, y + height/2))
    display.blit(text_surf, text_rect)

def draw_score(score, display):
    score_text = f"分数: {score}"
    score_surf = FONT_STYLE.render(score_text, True, BLACK)
    display.blit(score_surf, [10, 10])  # 在左上角显示分数

# 删除顶部所有字体初始化代码
# 保留以下函数定义...

def init_font():
    global FONT_STYLE
    try:
        FONT_STYLE = pygame.font.Font("/System/Library/Fonts/Supplemental/STHeiti Medium.ttf", 25)
    except:
        try:
            FONT_STYLE = pygame.font.SysFont("STHeiti Medium", 25)  # 使用系统预装苹方字体
        except:
            FONT_STYLE = pygame.font.Font(None, 25)

# 在game.py中调用init_font()