import random

import pygame

import constants
from game.bullet import Bullet


class Plane(pygame.sprite.Sprite):
    """飞机类的基类"""
    # 飞机图片路径列表
    plane_images = []
    # 飞机爆炸图片路径列表
    plane_destroy_images = []
    # 飞机坠毁音乐
    down_sound_src = None
    # 飞机的状态，存活-True，坠毁-False
    active = True
    # 飞机发射的子弹精灵组
    bullets = pygame.sprite.Group()

    # 飞机初始化
    def __init__(self, screen, speed=None):
        # 调用精灵父类方法
        super().__init__()
        # 获取游戏屏幕对象
        self.screen = screen
        # 飞行速度
        self.speed = speed or 10
        # 加载静态资源
        self._img_list = []
        self._destroy_img_list = []
        self.down_sound = None
        self.load_src()
        # 获取飞机位置
        self.rect = self._img_list[0].get_rect()
        # 获取飞机的宽、高
        self.width, self.height = self._img_list[0].get_size()
        # 获取屏幕的宽、高
        self.s_width, self.s_height = self.screen.get_size()

    def load_src(self):
        """加载静态资源"""
        # 加载飞机图片
        for img in self.plane_images:
            self._img_list.append(pygame.image.load(img))
        # 加载坠毁图片
        for img in self.plane_destroy_images:
            self._destroy_img_list.append(pygame.image.load(img))
        # 加载坠毁音乐
        self.down_sound = pygame.mixer.Sound(self.down_sound_src)

    @property
    def image(self):
        """以属性方式获取飞机图片对象"""
        return self._img_list[0]

    def blit_me(self):
        """屏幕中绘画本架飞机"""
        self.screen.blit(self.image, self.rect)

    def move_up(self):
        """向上移动"""
        self.rect.top -= self.speed

    def move_down(self):
        """向下移动"""
        self.rect.top += self.speed

    def move_left(self):
        """向左移动"""
        self.rect.left -= self.speed

    def move_right(self):
        """向右移动"""
        self.rect.left += self.speed

    def broken_down(self):
        """飞机坠毁"""
        # 播放坠毁音乐
        if self.down_sound:
            self.down_sound.play()
        # 播放坠毁动画
        for img in self._destroy_img_list:
            self.screen.blit(img, self.rect)
        # 坠毁后，设置飞机状态
        self.active = False

    def shoot(self):
        """飞机射击"""
        self.bullets.add(Bullet(self, 15))


class OurPlane(Plane):
    """我方飞机类"""
    # 设置一系列静态资源
    plane_images = constants.OUR_PLANE_IMAGES
    plane_destroy_images = constants.OUR_PLANE_DESTROY_IMAGES
    down_sound_src = constants.OUR_PLANE_DESTROY_SOUND

    def __init__(self, screen, speed=None):
        super().__init__(screen, speed)
        # 设置我方飞机的初始位置
        self.rect.top = int((self.s_height - self.height) / 2)
        self.rect.left = int((self.s_width - self.width) / 2)

    def update(self, war):
        """
        更新飞机的动画效果
        :param war: 飞机大战对象
        """
        # 键盘操作优化
        self.move(war.key_down)
        # 更新喷气效果
        if war.frame % 5:
            self.screen.blit(self._img_list[0], self.rect)
        else:
            self.screen.blit(self._img_list[1], self.rect)
        # 进行碰撞检测
        result = pygame.sprite.spritecollide(self, war.enemies, False)
        if result:
            # 当发生碰撞时
            # 1.清除所有敌方精灵组中的精灵
            war.enemies.empty()
            war.small_enemy_planes.empty()
            # 2.播放坠机效果
            self.broken_down()
            # 3.更新游戏状态
            war.status = war.GAME_OVER
            # 4.记录游戏分数
            pass

    """我方飞机，移动需要限定边界，因此需要重写一下父类方法"""
    def move_up(self):
        super().move_up()
        if self.rect.top < 0:
            self.rect.top += self.speed

    def move_down(self):
        super().move_down()
        if self.rect.top > self.s_height - self.height:
            self.rect.top -= self.speed

    def move_left(self):
        super().move_left()
        if self.rect.left < 0:
            self.rect.left += self.speed

    def move_right(self):
        super().move_right()
        if self.rect.left > self.s_width - self.width:
            self.rect.left -= self.speed

    def move(self, key):
        """移动优化"""
        if key == pygame.K_w or key == pygame.K_UP:
            self.move_up()
        elif key == pygame.K_s or key == pygame.K_DOWN:
            self.move_down()
        elif key == pygame.K_a or key == pygame.K_LEFT:
            self.move_left()
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            self.move_right()
        elif key == pygame.K_SPACE:
            self.shoot()


class SmallEnemyPlane(Plane):
    """敌方小型飞机"""
    # 敌方小型飞机图片路径列表
    plane_images = constants.SMALL_ENEMY_PLANE_IMAGES
    # 敌方小型飞机爆炸图片路径列表
    plane_destroy_images = constants.SMALL_ENEMY_PLANE_DESTROY_IMAGES
    # 敌方小型飞机坠毁音乐
    down_sound_src = constants.SMALL_ENEMY_PLANE_DESTROY_SOUND

    def __init__(self, screen, speed=None):
        """敌方小型飞机初始化"""
        super().__init__(screen, speed)
        # 设置敌方小型飞机的出现位置
        self.init_position()

    def update(self):
        """更新敌方小飞机， 此方法来自精灵父类"""
        # 更新敌方小型飞机的位置
        self.rect.top += self.speed
        self.screen.blit(self.image, self.rect)
        # 当超出屏幕时，将小飞机重用（这里也可以用多线程，后面有兴趣再改进）
        if self.rect.top > self.s_height:
            self.active = False
            self.reset()

    def reset(self):
        """重置小飞机"""
        self.init_position()
        self.active = True

    def init_position(self):
        """初始画小飞机位置"""
        self.rect.top = (- random.randint(1, 6) * self.height)
        self.rect.left = random.randint(0, self.s_width - self.width)

    def broken_down(self):
        """
        坠毁方法：这里重写父类方法是因为目前小型飞机坠毁后需要重置
        :return:
        """
        super().broken_down()
        self.reset()
