import os

# 获取项目路径
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 静态文件目录路径
STATIC_DIR = os.path.join(BASE_DIR, 'static')
# 图片文件目录路径
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')
# 音频文件目录路径
SOUNDS_DIR = os.path.join(STATIC_DIR, 'sounds')
# 分数文件目录路径
STORE_DIR = os.path.join(BASE_DIR, 'store')
# 背景图片
BG_IMG = os.path.join(IMAGES_DIR, 'background.png')
# 游戏开始标题
GAME_START_TITLE_IMG = os.path.join(IMAGES_DIR, 'game_title.png')
# 游戏开始按钮
GAME_START_BTN_IMG = os.path.join(IMAGES_DIR, 'game_start.png')

# 背景音乐
BG_MUSIC = os.path.join(SOUNDS_DIR, 'game_bg_music.wav')

# 游戏得分颜色
SCORE_COLOR = pygame.Color(0, 0, 0)
# 击中小飞机得分
SHOOT_SCORE_SMALL = 10
# 游戏历史分数记录文件
HISTORY_SCORE_FILE = os.path.join(STORE_DIR, 'score.text')

# 我方飞机图片列表
OUR_PLANE_IMAGES = [
    os.path.join(IMAGES_DIR, 'hero1.png'),
    os.path.join(IMAGES_DIR, 'hero2.png')
]
# 我方飞机坠毁图片列表
OUR_PLANE_DESTROY_IMAGES = [
    os.path.join(IMAGES_DIR, 'hero_broken_n1.png'),
    os.path.join(IMAGES_DIR, 'hero_broken_n2.png'),
    os.path.join(IMAGES_DIR, 'hero_broken_n3.png'),
    os.path.join(IMAGES_DIR, 'hero_broken_n4.png')
]
# 我方飞机坠毁音乐
OUR_PLANE_DESTROY_SOUND = os.path.join(SOUNDS_DIR, 'game_over.wav')
# 我方子弹图像
OUR_BULLET_IMG = os.path.join(IMAGES_DIR, 'bullet1.png')
# 我方子弹音乐
BULLET_SOUND = os.path.join(SOUNDS_DIR, 'bullet.wav')

# 敌方小型飞机图片列表
SMALL_ENEMY_PLANE_IMAGES = [
    os.path.join(IMAGES_DIR, 'enemy1.png')
]
# 敌方小型飞机坠机图片列表
SMALL_ENEMY_PLANE_DESTROY_IMAGES = [
    os.path.join(IMAGES_DIR, 'enemy1_down1.png'),
    os.path.join(IMAGES_DIR, 'enemy1_down2.png'),
    os.path.join(IMAGES_DIR, 'enemy1_down3.png'),
    os.path.join(IMAGES_DIR, 'enemy1_down4.png')
]
# 敌方小型飞机坠机音效
SMALL_ENEMY_PLANE_DESTROY_SOUND = os.path.join(SOUNDS_DIR, 'enemy1_down.wav')

# 游戏结束画面
GAME_OVER_IMAGE = os.path.join(IMAGES_DIR, 'game_over.png')
