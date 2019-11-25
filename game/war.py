import sys
import pygame

import constants
from game.plane import OurPlane, SmallEnemyPlane
from store.result import PlaneResult


class PlaneWar(object):
    """飞机大战程序执行类"""

    # 定义游戏状态常量
    READY = 0
    PLAYING = 1
    GAME_OVER = 2

    def __init__(self):
        # 游戏初始化
        pygame.init()
        """屏幕设定"""
        # 设置屏幕大小,这里根据游戏背景图片大小即可
        self.width, self.height = 480, 852
        # 获取屏幕对象
        self.screen = pygame.display.set_mode((self.width, self.height))
        # 设置屏幕标题
        pygame.display.set_caption('飞机大战')

        """图片设定"""
        # 加载背景图片,获取背景surface对象
        self.bg_img = pygame.image.load(constants.BG_IMG)
        # 加载游戏开始标题, 设置图片位置
        self.game_start_title = pygame.image.load(constants.GAME_START_TITLE_IMG)
        self.game_start_title_rect = self.game_start_title.get_rect()
        t_width, t_height = self.game_start_title.get_size()
        self.game_start_title_rect.topleft = (int((self.width - t_width) / 2), int((self.height / 2 - t_height)))
        # 加载游戏开始按钮，设置按钮位置
        self.game_start_btn = pygame.image.load(constants.GAME_START_BTN_IMG)
        self.game_start_btn_rect = self.game_start_btn.get_rect()
        b_width, b_height = self.game_start_btn.get_size()
        self.game_start_btn_rect.topleft = (int((self.width - b_width) / 2), int((self.height / 2 + b_height)))
        # 加载游戏结束图片
        self.game_over_img = pygame.image.load(constants.GAME_OVER_IMAGE)
        # 加载得分字体
        self.score_font = pygame.font.SysFont("songtittc", 21, False, False)

        """音乐设定"""
        self.play_bg_music()

        """游戏状态设定"""
        self.status = self.READY

        """调节主循环运行帧数"""
        # 获取游戏时钟对象
        self.clock = pygame.time.Clock()
        # 设置主循环计数变量
        self.frame = 0

        """创建我方飞机"""
        # 创建我方飞机
        self.our_plane = OurPlane(self.screen)

        """创建敌方飞机"""
        # 创建敌方精灵组
        self.enemies = pygame.sprite.Group()
        # 创建敌方小型飞机精灵族
        self.small_enemy_planes = pygame.sprite.Group()

        """创建游戏结果实例"""
        self.result = PlaneResult()

        """上一次键盘按键，用于移动优化"""
        self.key_down = None

    @staticmethod
    def play_bg_music():
        """加载并播放背景音乐"""
        # 加载背景音乐
        pygame.mixer.music.load(constants.BG_MUSIC)
        # 设置背景音乐音量为20%
        pygame.mixer.music.set_volume(0.2)
        # 背景音乐循环播放
        pygame.mixer.music.play(-1)

    def create_small_enemy_planes(self, num):
        """
        # 循环创建num架敌方小型飞机，并放入到精灵组中
        :param num: 敌方小型飞机数量
        :return:
        """
        for i in range(num):
            small_enemy_plane = SmallEnemyPlane(self.screen)
            # add方法为pygame的精灵类方法，目的是将小型飞机放入精灵组中
            small_enemy_plane.add(self.small_enemy_planes, self.enemies)

    def run_game(self):
        """运行游戏"""
        while True:
            # 控制帧数,每秒60帧
            self.clock.tick(60)

            # 计数
            self.frame += 1
            if self.frame > 60:
                self.frame = 0

            # 处理游戏事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # 当游戏处于准备状态时，点击鼠标游戏开始
                    if self.status == self.READY:
                        self.status = self.PLAYING
                    # 当游戏处于结束转改，点击鼠标则重新开始
                    elif self.status == self.GAME_OVER:
                        # 消除我方子弹
                        self.our_plane.bullets.empty()
                        # 创建六架飞机
                        self.create_small_enemy_planes(6)
                        # 消除键盘记录
                        pass
                        # 更新游戏状态
                        self.status = self.PLAYING
                elif event.type == pygame.KEYDOWN:
                    # 监视键盘，当在游戏进行状态下按下键盘时，作出对应操作
                    if self.status == self.PLAYING:
                        # 记录键盘按钮
                        self.key_down = event.key
                        if event.key == pygame.K_w or event.key == pygame.K_UP:
                            self.our_plane.move_up()
                        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            self.our_plane.move_down()
                        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            self.our_plane.move_left()
                        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            self.our_plane.move_right()
                        elif event.key == pygame.K_SPACE:
                            self.our_plane.shoot()
                elif event.type == pygame.KEYUP:
                    # 清除上一次键盘按钮记录
                    self.key_down = None

            # 更新游戏状态
            if self.status == self.READY:
                # 屏幕加载背景、标题、开始按钮
                self.screen.blit(self.bg_img, self.bg_img.get_rect())
                self.screen.blit(self.game_start_title, self.game_start_title_rect)
                self.screen.blit(self.game_start_btn, self.game_start_btn_rect)
            elif self.status == self.PLAYING:
                # 屏幕加载背景
                self.screen.blit(self.bg_img, self.bg_img.get_rect())
                # 绘制我方飞机
                self.our_plane.blit_me()
                # 更换我方飞机图片造成动态效果
                self.our_plane.update(self)
                # 绘制、更新子弹
                self.our_plane.bullets.update(self)
                # 绘制、更新敌方小型飞机
                self.small_enemy_planes.update()
                # 绘制得分
                score_text = self.score_font.render("得分: {0}".format(self.result.score), False, constants.SCORE_COLOR)
                self.screen.blit(score_text, score_text.get_rect())
            elif self.status == self.GAME_OVER:
                # 绘制游戏结束画面
                self.screen.blit(self.game_over_img, self.game_over_img.get_rect())
                # 绘制目前得分
                score_text = self.score_font.render("{0}分".format(self.result.score), False, constants.SCORE_COLOR)
                score_rect = score_text.get_rect()
                s_width, s_height = score_text.get_size()
                score_rect.topleft = (
                    int((self.width - s_width) / 2),
                    int(self.height / 2)
                )
                self.screen.blit(score_text, score_rect)
                # 记录游戏最高分
                self.result.record_highest_score()
                # 绘制游戏历史最高分
                history_score_text = self.score_font.render("{0}分".format(self.result.get_history_score()), False, constants.SCORE_COLOR)
                history_score_rect = history_score_text.get_rect()
                history_score_rect.topleft = (150, 40)
                self.screen.blit(history_score_text, history_score_rect)

            # 展示屏幕
            pygame.display.flip()
