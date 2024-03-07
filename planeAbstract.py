import pygame
import random
import time
from pygame.locals import *

'''
 1:实现飞机的显示 并且可以控制飞机的移动
'''


# 抽象一个基类
class BasePlane(object):
    def __init__(self, screen, imagePath):
        '''
        初始化基类
        :param screen: 主窗体对象
        :param imageName: 加载的图片
        '''
        self.screen = screen
        self.image = pygame.image.load(imagePath)
        self.bulletList = []

    pass

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        # 完善子弹的展示逻辑
        needDelItemList = []
        for item in self.bulletList:
            if item.judge():
                needDelItemList.append(item)
                pass
            pass

        # 遍历删除失效子弹
        for i in needDelItemList:
            self.bulletList.remove(i)
            pass

        for bullet in self.bulletList:
            # 显示子弹的位置
            bullet.display()
            # 子弹进行移动，下次再显示的就是子弹修改后的位置
            bullet.move()
            pass
        pass


class CommonBullet(object):
    '''
    公共子弹类
    '''
    def __init__(self, x, y, screen, bulletType):
        self.type = bulletType
        self.screen = screen

        if self.type == 'hero':
            self.x = x + 10
            self.y = y - 10
            self.imagePath = './plane/zidan1.png'
            pass
        elif self.type == 'enemy':
            self.x = x + 5
            self.y = y + 10
            self.imagePath = './plane/zidan2.png'
            pass
        self.image = pygame.image.load(self.imagePath)
        pass

    def move(self):
        '''
        子弹的移动
        :return:
        '''
        if self.type == 'hero':
            self.y -= 2
        elif self.type == 'enemy':
            self.y += 2
        pass

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        pass

    def judge(self):
        '''
        判断子弹是否越界
        :return:
        '''
        if self.y > 500 or self.y < 0:
            return True
        else:
            return False
        pass


class HeroPlane(BasePlane):
    def __init__(self, screen):
        '''
        :param screen:主窗体对象
        初始化函数
        '''
        super().__init__(screen, './plane/feiji1.png')

        # 飞机的默认位置
        self.x = 150
        self.y = 460

    def moveLeft(self):
        '''
        左移动
        :return:
        '''
        if self.x > 0:
            self.x -= 10
        pass

    def moveRight(self):
        '''
        右移动
        :return:
        '''
        if self.x < 300:
            self.x += 10
        pass

    # 发射子弹
    def shotBullet(self):
        # 创建一个子弹对象
        newBullet = CommonBullet(self.x, self.y, self.screen, 'hero')
        self.bulletList.append(newBullet)
        pass


'''
创建敌机类
'''


class EnemyPlane(BasePlane):
    def __init__(self, screen):
        super().__init__(screen, './plane/enemy0.png')
        # 默认设置一个方向
        self.direction = 'right'
        # 设置飞机的默认位置
        self.x = 0
        self.y = -10

    # 发射子弹
    def shotBullet(self):
        # 敌机随机发射子弹
        num = random.randint(1, 100)
        if num == 3:
            newBullet = CommonBullet(self.x, self.y, self.screen, 'enemy')
            self.bulletList.append(newBullet)
            pass
        pass

    def move(self):
        '''
        敌机移动 随机
        :return:
        '''
        if self.direction == 'right':
            self.x += 0.5
            pass
        elif self.direction == 'left':
            self.x -= 0.5
            pass

        if self.x > 330:
            self.direction = 'left'
        elif self.x < 0:
            self.direction = 'right'
        pass


def key_control(HeroObj):
    '''
    定义普通函数 用来实现键盘的检测
    :param HeroObj:
    :return:
    '''
    eventList = pygame.event.get()
    for event in eventList:
        if event.type == QUIT:
            print('退出')
            exit()
            pass
        elif event.type == KEYDOWN:
            if event.type == K_a or event.key == K_LEFT:
                print('left')
                HeroObj.moveLeft()
                pass
            elif event.type == K_d or event.key == K_RIGHT:
                print('right')
                HeroObj.moveRight()
                pass
            elif event.key == K_SPACE:
                print('按下空格键')
                HeroObj.shotBullet()


def main():
    # 创建一个窗口用来显示内容
    screen = pygame.display.set_mode((350, 500), depth=32)
    # 设定一个背景图片
    background = pygame.image.load('./plane/back.png')
    # 设定一个title
    pygame.display.set_caption('阶段总结-飞机游戏')
    # 添加背景音乐
    pygame.mixer.init()
    pygame.mixer.music.load('./plane/background.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)  # -1表示无限循环

    # 创建一个飞机对象
    hero = HeroPlane(screen)

    # 创建一个敌机对象
    enemyPlane = EnemyPlane(screen)

    # 设定要显示的内容
    while True:
        screen.blit(background, (0, 0))
        # 显示玩家飞机的图片
        hero.display()
        # 显示敌机
        enemyPlane.display()
        # 敌机移动
        enemyPlane.move()
        # 敌机发射子弹
        enemyPlane.shotBullet()
        # 获取键盘事件
        key_control(hero)
        # 更新显示的内容
        pygame.display.update()
        # pygame.time.Clock().tick(100)  # 1秒执行5次
    pass


if __name__ == '__main__':
    main()
