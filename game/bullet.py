import pygame

import constants


class Bullet(pygame.sprite.Sprite):
    """子弹类精灵"""
    def __init__(self, plane, speed=None):
        """子弹类初始化函数"""
        # 调用一波精灵父类初始化函数
        super().__init__()
        # 子弹的状态, True: 在屏幕有效区内
        self.active = True
        # 射出本子弹的飞机对象
        self.plane = plane
        # 子弹的速度
        self.speed = speed or 15
        # 获取屏幕对象
        self.screen = self.plane.screen
        # 加载子弹图像, 获取子弹初始位置
        self.image = pygame.image.load(constants.OUR_BULLET_IMG)
        self.rect = self.image.get_rect()
        # 设置子弹出现位置
        self.width, self.height = self.image.get_size()
        self.rect.centerx = self.plane.rect.centerx
        self.rect.top = self.plane.rect.top + self.height

        # 加载子弹音效，播放
        self.sound = pygame.mixer.Sound(constants.BULLET_SOUND)
        self.play_music()

    def play_music(self):
        """
        子弹音乐播放函数
        """
        self.sound.set_volume(0.4)
        self.sound.play()

    def update(self, war):
        """
        更新子弹，此方法继承自精灵类
        :param war: 飞机大战对象
        """
        # 绘制子弹，更新子弹位置
        self.screen.blit(self.image, self.rect)
        self.rect.top -= self.speed
        # 当子弹超出界面时，去除子弹精灵
        if self.rect.top < 0:
            # 此remove函数来自精灵父类，语法为remove(精灵组对象)
            self.remove(self.plane.bullets)
        # 子弹碰撞检测
        result = pygame.sprite.spritecollide(self, war.enemies, False)
        for r in result:
            # 碰撞后让子弹消失，kill函数来自精灵父类，用于消灭该精灵
            self.kill()
            # 让小型飞机坠毁
            r.broken_down()
            # 记录分数
            war.result.score += constants.SHOOT_SCORE_SMALL






